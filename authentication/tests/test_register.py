from api.tests import (
    User, APITestCase,
    mixer, reverse, status, mail
)


class RegisterAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("api_v1:authentication:register")

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, resp.status_code)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_data(self):
        resp = self.client.post(self.url)

        data = {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'password1': ['This field is required.'],
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.']
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_username_exist(self):

        mixer.blend(User, username="test")

        data = {
            'username': "test",
            "password": "django123",
            "password1": "django123",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data=data)

        data = {'username': ['A user with that username already exists.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_password_not_match(self):
        data = {
            'username': "test",
            "password": "django123",
            "password1": "django1234",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data)

        data = {'password': ["Password fields didn't match."]}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_password_min_length(self):
        data = {
            'username': "test",
            "password": "dj",
            "password1": "dj",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data)
        data = {'password': ['This password is too short. It must contain at least 8 characters.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_password_numeric(self):
        data = {
            'username': "test",
            "password": "12345678",
            "password1": "12345678",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data)

        data = {'password': ['This password is too common.', 'This password is entirely numeric.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_password_similarity(self):
        data = {
            'username': "test",
            "password": "test1234",
            "password1": "test1234",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data)

        data = {'password': ['This password is too common.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_email_exist(self):
        mixer.blend(User, email="test@test.com")

        data = {
            'username': "test",
            "password": "django123",
            "password1": "django123",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }

        resp = self.client.post(self.url, data)

        data = {'message': ['This email already taken!']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_register_success(self):
        data = {
            'username': "test",
            "password": "django123",
            "password1": "django123",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com"
        }
        mail.outbox = []

        resp = self.client.post(self.url, data)

        u = User.objects.last()

        user_data = {
            'username': u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "is_email_verified": u.is_email_verified
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['user'], user_data)
        self.assertEqual(mail.outbox[0].to, [u.email])
        self.assertIsNotNone(resp.json()['token'])


