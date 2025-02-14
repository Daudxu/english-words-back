from app.db.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = UserRepository(db)

    def create_user(self, user: UserCreate) -> UserResponse:
        return self.repository.create_user(user)