# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api.v1.routers import api_router
from app.middleware.jwt_middleware import JWTMiddleware  # 导入中间件
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
# 创建 FastAPI 应用
app = FastAPI(title="App")

# 添加 CORS 中间件

# 配置 CORS 中间件
origins = [
    # "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # 允许的来源列表
    allow_origins=["*"],  # 允许的来源列表
    allow_credentials=True,  # 是否允许发送 Cookie
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 明确列出允许的方法
    allow_headers=["Content-Type", "Authorization"],      # 允许所有的请求头
)


# 将 JWT 校验中间件添加到 FastAPI 应用中
app.add_middleware(JWTMiddleware)

# 将 api_router 添加到应用中，并设置 API 路由前缀
app.include_router(api_router, prefix="/api/v1")

# 打印所有路由，检查是否注册成功
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")

# --- LangGraph 配置和初始化 ---
load_dotenv()
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

llm = ChatOpenAI(
    base_url=MODEL_BASE_URL,
    api_key=MODEL_API_KEY,
    model=MODEL_NAME,
    temperature=0.1,
    max_tokens=512,
    streaming=True
)

SYSTEM_PROMPT_TEMPLATE = '''你是一位专业的英语单词学习助手，当前学习单词为“{word}”。
【对话规则】
- 首次进入时，只输出：同学你好，针对单词“{word}”，还有什么想要了解的，我可以为你详细讲解哦~你也可以点击对话框上方的选项来进行提问。不要输出释义、用法、搭配等内容。
- 用户输入的内容如果不是“{word}”，无论是其他英文单词还是其他内容，都只回复：咱们还是专注于“{word}”这个单词吧，你在这个单词上还有什么疑问吗？
- 只有当用户输入“{word}”时，才输出该单词的简明中文释义，并以“你理解这个意思了吗？”结尾。例如：“这个单词的意思是‘男孩’，你理解这个意思了吗？”
- 用户输入“详细用法”时，只输出1~2种常见用法，举例说明，并以“你理解了吗？”结尾，不要输出多余拓展。
- 用户输入“固定搭配”时，只列举常见搭配，举例说明，并以“你记住这个搭配了吗？”结尾。
- 用户输入“词根词缀”时，只说明有无词根词缀，简要解释，并以“现在你理解了吗？”结尾。
- 用户输入“例句”时，只输出1个例句，并以“你能理解这个例句中‘{word}’的用法吗？”结尾。
- 用户输入“选择题”或“出一道选择题”时，只设计一道选择题，并以“请选择A、B或C。你能找出正确答案吗？”结尾。
- 用户输入A/B/C时，只判断正误并回复。

【输出要求】
- 只允许输出纯文本、结构化简明内容，禁止输出任何 markdown、表格、代码块、分点说明、mermaid、emoji、拓展知识、文化背景等。
- 每次回复只聚焦用户当前问题，不要重复输出全部知识点。
- 欢迎语只输出一次，后续不再重复。'''

class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    word: str

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT_TEMPLATE),
    MessagesPlaceholder(variable_name="messages"),
])
llm_chain = prompt | llm

def llm_node_chat(state: ChatState) -> ChatState:
    current_messages = state["messages"]
    current_word = state["word"]
    ai_response = llm_chain.invoke({"messages": current_messages, "word": current_word})
    if isinstance(ai_response.content, str):
        processed_content = ai_response.content.replace("{word}", current_word)
        processed_ai_response = AIMessage(content=processed_content)
    else:
        processed_ai_response = ai_response
    return {"messages": [processed_ai_response]}

def check_quit_node(state: ChatState) -> ChatState:
    return {}

def route_decision(state: ChatState) -> str:
    current_messages = state["messages"]
    last_human_message = None
    for msg in reversed(current_messages): 
        if isinstance(msg, HumanMessage):
            last_human_message = msg
            break
    if last_human_message and last_human_message.content.lower() in ["退出", "exit"]:
        return "END"
    else:
        return "llm_node"

workflow = StateGraph(ChatState)
workflow.add_node("llm_node", llm_node_chat)
workflow.add_node("check_quit_node", check_quit_node)
workflow.set_entry_point("check_quit_node")
workflow.add_conditional_edges(
    "check_quit_node",
    route_decision,
    {
        "llm_node": "llm_node",
        "END": END
    }
)
workflow.add_edge("llm_node", END)
langgraph_app = workflow.compile()

@app.websocket("/api/v1/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 第一步：等待客户端发送 word
        await websocket.send_text("请输入你要学习的单词：")
        word = await websocket.receive_text()
        chat_history_for_connection = {"messages": [], "word": word}
        # 首次自动触发欢迎语
        try:
            initial_invoke_state = {"messages": [HumanMessage(content="")], "word": word}
            result_state_greeting = langgraph_app.invoke(initial_invoke_state)
            greeting_message = result_state_greeting["messages"][-1].content
            await websocket.send_text(greeting_message)
            chat_history_for_connection = result_state_greeting
        except Exception as e:
            await websocket.send_text("抱歉，初始化聊天时发生错误。请重试。")
            await websocket.close()
            return
        # 循环收发消息
        while True:
            user_input_content = await websocket.receive_text()
            if user_input_content.lower() in ["退出", "exit"]:
                await websocket.send_text("再见！对话已结束。")
                break
            chat_history_for_connection["messages"].append(HumanMessage(content=user_input_content))
            result_state = langgraph_app.invoke(chat_history_for_connection)
            chat_history_for_connection = result_state
            ai_response_message = chat_history_for_connection["messages"][-1]
            if isinstance(ai_response_message, AIMessage):
                await websocket.send_text(ai_response_message.content)
            else:
                await websocket.send_text("抱歉，未能获取有效回复。")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        await websocket.close()

# 如果你运行应用，使用以下命令启动：
# uvicorn app.main:app --reload