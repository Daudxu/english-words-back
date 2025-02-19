# app/db/models/user_guide.py
from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP
from app.db.session import Base  # 导入你已有的Base类

class UserGuideDoc(Base):
    __tablename__ = 'tb_user_guide_docs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('privacy_policy', 'user_agreement', 'contact_info'), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
