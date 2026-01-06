from api.tests import (
    User, APITestCase,
    mixer, reverse, status,
    dummy_token, timedelta, now, mail,
    settings
)


class VerifyAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:authentication:verify_email")
        self.user = mixer.blend(User, is_email_verified=False, email="admin@admin.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {dummy_token(self.user)}")

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_data(self):

        resp = self.client.post(self.url)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, {'message': 'Invalid data sent!'})

    def test_invalid_code(self):
        resp = self.client.post(self.url, data={"code": "-------"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, {'message': 'Invalid verification code'})

    def test_email_already_verified(self):
        self.user.is_email_verified = True
        self.user.verification_code = "123"
        self.user.save()

        resp = self.client.post(self.url, data={"code": "123"})

        data = {'message': 'Your email already verified!'}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_code_expired_days(self):
        self.user.verification_code = "123"
        self.user.expire_verification_code = now() - timedelta(days=1)
        self.user.save()

        resp = self.client.post(self.url, data={"code": "123"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, {'message': 'Your code was expired'})

    def test_code_expired_minutes(self):
        self.user.verification_code = "123"
        self.user.expire_verification_code = now() - timedelta(minutes=1)
        self.user.save()

        resp = self.client.post(self.url, data={"code": "123"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, {'message': 'Your code was expired'})

    def test_code_expired_seconds(self):
        self.user.verification_code = "123"
        self.user.expire_verification_code = now() - timedelta(seconds=1)
        self.user.save()

        resp = self.client.post(self.url, data={"code": "123"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, {'message': 'Your code was expired'})

    def test_email_verified_success(self):
        self.user.verification_code = "123"
        self.user.expire_verification_code = now() + timedelta(minutes=1)
        self.user.save()

        resp = self.client.post(self.url, data={"code": "123"})

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, {'message': 'Successfully verified'})


class ResendEmailVerifiedAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:authentication:resend_email")
        self.user = mixer.blend(User, is_email_verified=False, email="admin@admin.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {dummy_token(self.user)}")

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_email_already_verified(self):
        self.user.is_email_verified = True
        self.user.save()

        resp = self.client.get(self.url)

        data = {'message': 'Your email already verified'}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_email_verified_success(self):

        mail.outbox = []
        resp = self.client.get(self.url)

        data = {'message': 'Email has been sent. Please check your mailbox.'}
        mail_data = mail.outbox[0]

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)
        self.assertEqual(mail_data.to, [self.user.email])
        self.assertIn(settings.APP_NAME.capitalize(), mail_data.subject)
        self.assertIn("Email Verification", mail_data.subject)
