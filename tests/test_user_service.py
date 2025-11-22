import unittest
from unittest.mock import Mock
from models.user import User
from services.user_service import UserService
from repositories.base import UserRepository


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=UserRepository)
        self.service = UserService(self.mock_repo)

    def test_create_new_user(self):
        self.mock_repo.get_user_by_email.return_value = None
        fake_user = User(id=1, name="Анна", email="anna@example.com", created_at=None)
        self.mock_repo.create_user.return_value = fake_user

        user = self.service.create_user("Анна", "anna@example.com")

        self.assertEqual(user.name, "Анна")
        self.assertEqual(user.email, "anna@example.com")
        self.mock_repo.get_user_by_email.assert_called_once_with("anna@example.com")
        self.mock_repo.create_user.assert_called_once_with("Анна", "anna@example.com")

    def test_email_already_exists(self):
        existing_user = User(id=1, name="Борис", email="boris@example.com", created_at=None)
        self.mock_repo.get_user_by_email.return_value = existing_user

        with self.assertRaises(ValueError) as context:
            self.service.create_user("Борис", "boris@example.com")

        self.assertEqual(str(context.exception), "User with this email already exists")
        self.mock_repo.get_user_by_email.assert_called_once_with("boris@example.com")
        self.mock_repo.create_user.assert_not_called()


if __name__ == '__main__':
    unittest.main()