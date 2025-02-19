# app/services/user_guide.py
from sqlalchemy.orm import Session
from app.db.models.user_guide import UserGuideDoc
from app.schemas.user_guide import UserGuideResponse

class UserGuideService:
    @staticmethod
    def get_user_guide(db: Session, guide_type: str) -> UserGuideResponse:
        # 查询数据库获取相应内容
        guide = db.query(UserGuideDoc).filter(UserGuideDoc.type == guide_type).first()

        if not guide:
            return None
        
        return UserGuideResponse(title=guide.title, content=guide.content)
