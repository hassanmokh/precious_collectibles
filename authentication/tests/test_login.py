from api.tests import (
    User, APITestCase,
    mixer, reverse, status
)


class LoginAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("api_v1:authentication:login")

    def test_invalid_data(self):
        resp = self.client.post(self.url)

        data = {'username': ['This field is required.'], 'password': ['This field is required.']}

        self.assertTrue(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_username_or_password(self):
        user = mixer.blend(User, username='test')

        resp = self.client.post(self.url, data={"username": user.username, "password": "123"})

        data = {'non_field_errors': ['Unable to log in with provided credentials.']}
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, resp.status_code)
        self.assertJSONEqual(resp.content, data)

    def test_login_success(self):
        user = mixer.blend(User, username="test")
        user.set_password("django123")
        user.save()

        resp = self.client.post(self.url, data={"username": "test", "password": "django123"})

        data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_email_verified": user.is_email_verified
        }

        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(resp.json()['user'], data)
        self.assertIsNotNone(resp.json()['token'])

