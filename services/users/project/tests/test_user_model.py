import unittest

from sqlalchemy.exc import IntegrityError

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_user_model(self):
        user = add_user('justatest', 'test@test.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com')
        with self.assertRaises(IntegrityError):
            add_user('justatest', 'test@test2.com')

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com')
        with self.assertRaises(IntegrityError):
            add_user('justatest2', 'test@test.com')

    def test_to_json(self):
        user = add_user('justatest', 'test@test.com')
        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == "__main__":
    unittest.main()
