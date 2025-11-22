import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models.user import User
from repositories.base import UserRepository
from config import DATABASE_URL


class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.connection_params = DATABASE_URL

    def _get_connection(self):
        conn = psycopg2.connect(self.connection_params)
        conn.set_client_encoding('UTF8')
        return conn

    def create_user(self, name: str, email: str) -> User:
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email, created_at",
                        (name, email)
                    )
                    result = cur.fetchone()
                    return User(**result)
        except psycopg2.IntegrityError:
            raise ValueError("User with this email already exists")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "SELECT id, name, email, created_at FROM users WHERE email = %s",
                        (email,)
                    )
                    row = cur.fetchone()
                    return User(**row) if row else None
        except Exception as e:
            print(f"Error getting user by email {email}: {e}")
            return None

    def get_all_users(self) -> List[User]:
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
                    rows = cur.fetchall()
                    return [User(**row) for row in rows]
        except Exception as e:
            raise Exception(f"Failed to fetch users: {str(e)}")