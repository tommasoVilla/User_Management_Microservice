import unittest

from app import app


class TestUserLogin(unittest.TestCase):

    # By default in the DB an user with username admin and password admin_pass already exists
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Testing standard case: an user is found in data store
    def test_found_user(self):
        response = self.app.get('/user_management/api/v1.0/users/admin/admin_pass')
        self.assertEqual(200, response.status_code)

    # Testing wrong case: an user is not found in data store
    def test_not_found_user(self):
        response = self.app.get('/user_management/api/v1.0/users/admin/admin_wrong_pass')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
