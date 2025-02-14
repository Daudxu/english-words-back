from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserResponse

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserResponse:
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserResponse.from_orm(db_user)