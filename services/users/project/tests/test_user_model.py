import unittest

from sqlalchemy.exc import IntegrityError

from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com', 'test')
        with self.assertRaises(IntegrityError):
            add_user('justatest', 'test@test2.com', 'test')

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com', 'test')
        with self.assertRaises(IntegrityError):
            add_user('justatest2', 'test@test.com', 'test')

    def test_to_json(self):
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user1 = add_user('justatest', 'test@test.com', 'test')
        user2 = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(user1.password, user2.password)

    def test_encode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)


if __name__ == "__main__":
    unittest.main()