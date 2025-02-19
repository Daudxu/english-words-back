# from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, text
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "tb_users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    name = Column(String(100), default='', comment="姓名")
    phone = Column(String(255), unique=True, index=True, nullable=False, comment="手机号")
    password = Column(String(255), comment="密码")
    vip_start_time = Column(BigInteger, comment="VIP开始时间")
    vip_end_time = Column(BigInteger, comment="VIP结束时间")
    create_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment="创建时间")
    update_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), 
                      onupdate=text('CURRENT_TIMESTAMP'), comment="更新时间")

    # 如果需要字段别名可以添加
    @property
    def created_at(self):
        return self.create_at

    @property
    def updated_at(self):
        return self.update_at