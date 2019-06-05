import unittest
import boto3

from app import app


class TestUserRegistration(unittest.TestCase):

    # By default in the DB an user with username admin already exists
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Testing standard case: an user complete his registration
    def test_insert_user(self):
        content = {'name': 'nome',
                   'surname': 'cognome',
                   'username': 'username',
                   'password': 'password',
                   'fiscalCode': 'student'}
        response = self.app.post('/user_management/api/v1.0/users', json=content)
        self.assertEqual(201, response.status_code)

    # Testing inserting attempt of an user with existing username
    def test_conflict_insert(self):
        content = {'name': 'nome',
                   'surname': 'cognome',
                   'username': 'admin',
                   'password': 'password',
                   'fiscalCode': 'student'}
        response = self.app.post('/user_management/api/v1.0/users', json=content)
        self.assertEqual(409, response.status_code)

    # Testing forwarding of a request with lacking fields
    def test_bad_request_incomplete(self):
        content = {'username': 'username1',
                   'password': 'password1'}
        response = self.app.post('/user_management/api/v1.0/users', json=content)
        self.assertEqual(400, response.status_code)

    # Testing forwarding of a request with invalid type
    def test_bad_request_type(self):
        content = {'name': '23',
                   'surname': 'cognome',
                   'username': 'username',
                   'password': 'password',
                   'fiscalCode': 'student'}
        response = self.app.post('/user_management/api/v1.0/users', json=content)
        self.assertEqual(400, response.status_code)

    # Testing registration attempt made by an unauthorized user
    def test_unauthorized_request(self):
        content = {'name': 'nome',
                   'surname': 'cognome',
                   'username': 'username2',
                   'password': 'password',
                   'fiscalCode': 'notsigned'}
        response = self.app.post('/user_management/api/v1.0/users', json=content)
        self.assertEqual(403, response.status_code)

    # The environment is cleaned eliminating the created item
    def tearDown(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        table.delete_item(
            Key={'Username': 'username'}
        )


if __name__ == '__main__':
    unittest.main()
