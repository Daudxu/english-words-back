from fastapi import APIRouter
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/", response_model=UserResponse)
def get_test_user():
    return {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com"
    }