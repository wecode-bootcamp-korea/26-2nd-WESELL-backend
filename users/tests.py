import jwt

from unittest.mock import MagicMock, patch
from django.test   import Client, TestCase

from users.models  import User
from wesell.settings import ALGORITHM, SECRET_KEY

class SigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            id    = 1,
            email = 'gjrbqls@gmail.com',
            kakao = 123456789,
        )

    def tearDown(self) :
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_signin_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 123456780, 
                    'kakao_account': { 'email' : 'gjrbqlsk@gmail.com' }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': '가짜 access_token'}
        response            = client.get('/users/signin', **headers)
        
        access_token = jwt.encode({'id': 5}, SECRET_KEY, algorithm=ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), { 'access_token' : access_token })

    @patch('users.views.requests')
    def test_kakao_signin_existing_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 123456789, 
                    'kakao_account': { 'email' : 'gjrbqls@gmail.com' }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': '가짜 access_token'}
        response            = client.get('/users/signin', **headers)

        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm=ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { 'access_token' : access_token })

    def test_kakao_signin_user_with_no_access_token_fail(self):
        client = Client()

        headers  = {}
        response = client.get('/users/signin', **headers)

        self.assertEqual(response.status_code, 400)