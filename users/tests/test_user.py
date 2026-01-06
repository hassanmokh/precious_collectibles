from api.tests import (
    User, APITestCase,
    mixer, reverse, status
)


class ListUsersAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:users:list_view")
        self.user = mixer.blend(User, is_email_verified=True, is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):

        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_list_users(self):
        u = mixer.blend(User)
        resp = self.client.get(self.url)

        data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'username': u.username,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'email': u.email,
                    'is_email_verified': u.is_email_verified
                },
                {
                    'username': self.user.username,
                    'first_name': self.user.first_name,
                    'last_name': self.user.last_name,
                    'email': self.user.email,
                    'is_email_verified': self.user.is_email_verified
                }
            ]
        }
        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class ChangePasswordAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:users:password_change")
        self.user = mixer.blend(User, is_email_verified=True, username="test")
        self.user.set_password("django1234")
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_old_password(self):

        data = {
            "old_password": "django12345",
            "password": "django123",
            "password1": "django123"
        }

        resp = self.client.patch(self.url, data=data)

        data = {'message': ['Incorrect the current password, Please enter the correct current password']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_password_didnt_match(self):
        data = {
            "old_password": "django1234",
            "password": "django1233",
            "password1": "django123"
        }

        resp = self.client.patch(self.url, data=data)

        data = {'message': ["Password fields didn't match"]}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_change_password(self):
        data = {
            "old_password": "django1234",
            "password": "django1234",
            "password1": "django1234"
        }

        resp = self.client.patch(self.url, data=data)

        data = {'message': ["You cannot change the password with the same current password"]}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_similarity_password(self):
        data = {
            "old_password": "django1234",
            "password": "test1234",
            "password1": "test1234"
        }

        resp = self.client.patch(self.url, data=data)

        data = {'password': ['This password is too common.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_numeric_password(self):
        data = {
            "old_password": "django1234",
            "password": "12345678",
            "password1": "12345678"
        }

        resp = self.client.patch(self.url, data=data)

        data = {'password': ['This password is too common.', 'This password is entirely numeric.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_min_length_password(self):
        data = {
            "old_password": "django1234",
            "password": "123",
            "password1": "123"
        }

        resp = self.client.patch(self.url, data=data)

        data = {
            'password': [
                'This password is too short. It must contain at least 8 characters.',
                'This password is too common.',
                'This password is entirely numeric.'
            ]
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_change_password_success(self):
        data = {
            "old_password": "django1234",
            "password": "djangp123",
            "password1": "djangp123"
        }

        resp = self.client.patch(self.url, data=data)

        data = {
            "message": "successfully updated"
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class MyInfoAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(User)
        self.url = reverse("api_v1:users:my_info")
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_get_my_info(self):

        resp = self.client.get(self.url)

        data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'is_email_verified': self.user.is_email_verified
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_update_first_name(self):

        resp = self.client.patch(self.url, data={"first_name": "tttt"})

        data = {
            'username': self.user.username,
            'first_name': "tttt",
            'last_name': self.user.last_name,
            'email': self.user.email,
            'is_email_verified': self.user.is_email_verified
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_update_last_name(self):

        resp = self.client.patch(self.url, data={"last_name": "tttt"})

        data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': "tttt",
            'email': self.user.email,
            'is_email_verified': self.user.is_email_verified
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_update_email_success(self):
        resp = self.client.patch(self.url, data={"email": "test@test.com"})

        data = {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': "test@test.com",
            'is_email_verified': False
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_email(self):
        mixer.blend(User, email="test@test.com")
        resp = self.client.patch(self.url, data={"email": "test@test.com"})

        data = {'email': {'message': 'This email already exists'}}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

