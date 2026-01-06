from api.tests import (
    User, APITestCase,
    mixer, reverse, status,
    dummy_token, timedelta
)


class LogoutAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("api_v1:authentication:logout")
        self.user = mixer.blend(User, is_active=True, is_email_verified=True)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {dummy_token(self.user)}")

    def test_method_not_allowed(self):

        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, resp.status_code)
        self.assertJSONEqual(resp.content, data)

    def test_logout_success(self):
        resp = self.client.get(self.url)

        data = {
            "message": "Successfully logout"
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_token(self):
        self.client.logout()

        resp = self.client.get(self.url)

        data = {'detail': 'Authentication credentials were not provided.'}

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_token_expired(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {dummy_token(self.user, timedelta(days=-1))}")

        resp = self.client.get(self.url)

        data = {'detail': 'Invalid token.'}

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertJSONEqual(resp.content, data)
