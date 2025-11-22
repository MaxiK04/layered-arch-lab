from abc import ABC, abstractmethod
from typing import List, Optional
from models.user import User
class UserRepository(ABC):
    @abstractmethod
    def create_user(self, name: str, email: str) -> User: pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
