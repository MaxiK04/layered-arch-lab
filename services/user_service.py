from typing import List, Optional
from models.user import User
from repositories.base import UserRepository

class UserService:
    def  __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    def register_user(self, name: str, email: str) -> User:
        if not email or "@" not in email:
            raise ValueError("Некорректный email")
        if self.user_repo.get_user_by_email(email):
            raise ValueError("Пользователь с таким email уже существует")
        return self.user_repo.create_user(name, email)

    def find_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_user_by_email(email)

    def list_all_users(self) -> List[User]:
        return self.user_repo.get_all_users()
