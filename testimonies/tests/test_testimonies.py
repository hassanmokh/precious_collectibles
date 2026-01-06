from api.tests import (
    APITestCase, Testimonies,
    status, mixer, create_file,
    reverse, shutil, settings
)


class ListTestimoniesAPITest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("api_v1:testimonies:list_testimonies")

    def test_method_not_allowed(self):

        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_empty_testimonies(self):

        resp = self.client.get(self.url)

        data = {'count': 0, 'next': None, 'previous': None, 'results': []}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_list_testimonies_success(self):
        test1 = mixer.blend(Testimonies)

        resp = self.client.get(self.url)

        data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': test1.id,
                    'created_at': test1.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': test1.is_deleted,
                    'updated_at': test1.updated_at.isoformat().replace('+00:00', 'Z'),
                    'image': f'http://testserver{test1.image.url}',
                    'full_name': test1.full_name,
                    'body': test1.body,
                    'screenshot': f'http://testserver{test1.screenshot.url}',
                    'testimony_date': str(test1.testimony_date)
                }
            ]
        }

        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_get_live_testimonies(self):
        mixer.blend(Testimonies, is_deleted=True)
        test1 = mixer.blend(Testimonies)

        resp = self.client.get(self.url)

        data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': test1.id,
                    'created_at': test1.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': test1.is_deleted,
                    'updated_at': test1.updated_at.isoformat().replace('+00:00', 'Z'),
                    'image': f'http://testserver{test1.image.url}',
                    'full_name': test1.full_name,
                    'body': test1.body,
                    'screenshot': f'http://testserver{test1.screenshot.url}',
                    'testimony_date': str(test1.testimony_date)
                }
            ]
        }

        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_delete_testimonies(self):
        mixer.blend(Testimonies, is_deleted=True)

        resp = self.client.get(self.url)

        data = {'count': 0, 'next': None, 'previous': None, 'results': []}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class RetrieveTestimonyAPITest(APITestCase):
    def setUp(self) -> None:
        self.testimony = mixer.blend(Testimonies, is_deleted=False)
        self.url = reverse("api_v1:testimonies:get_testimony", args=(self.testimony.id,))
        self.user = mixer.blend('users.User', is_staff=True, is_active=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_permission_denied(self):
        self.user.is_staff = False
        self.user.save()

        resp = self.client.post(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_not_found_testimony(self):
        self.testimony.is_deleted = True
        self.testimony.save()

        resp = self.client.get(self.url)

        data = {'detail': 'Not found.'}

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(resp.content, data)

    def test_get_testimony_success(self):
        resp = self.client.get(self.url)

        data = {
            'id': self.testimony.id,
            'created_at': self.testimony.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': self.testimony.is_deleted,
            'updated_at': self.testimony.updated_at.isoformat().replace('+00:00', 'Z'),
            'image': f'http://testserver{self.testimony.image.url}',
            'full_name': self.testimony.full_name,
            'body': self.testimony.body,
            'screenshot': f'http://testserver{self.testimony.screenshot.url}',
            'testimony_date': str(self.testimony.testimony_date)
        }

        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class CreateTestimoniesAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend('users.User', is_superuser=True, is_staff=True, is_active=True)
        self.client.force_authenticate(self.user)
        self.url = reverse("api_v1:testimonies:create_testimony")

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_permission_denied(self):
        self.user.is_staff = False
        self.user.save()

        resp = self.client.post(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_required_fields(self):

        resp = self.client.post(self.url)

        data = {
            'image': ['No file was submitted.'],
            'full_name': ['This field is required.'],
            'body': ['This field is required.'],
            'screenshot': ['No file was submitted.'],
            'testimony_date': ['This field is required.']
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_length_full_name(self):
        data = {
            'image': create_file(force_image=True),
            'full_name': 'te-tee',
            'body': 'welcome from testimonies',
            'screenshot': create_file(force_image=True),
            'testimony_date': '2023-03-03'
        }
        resp = self.client.post(self.url, data)

        data = {
            'full_name': {
                'message': 'Please enter the correct full name, The length of the full name should at least 6 characters contains alphabets and - only'
            }
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_create_testimony_success(self):
        data = {
            'image': create_file(force_image=True),
            'full_name': 'test test',
            'body': 'welcome from testimonies',
            'screenshot': create_file(force_image=True),
            'testimony_date': '2023-03-03'
        }

        resp = self.client.post(self.url, data)

        test1 = Testimonies.objects.last()

        data = {
            'id': test1.id,
            'created_at': test1.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': test1.is_deleted,
            'updated_at': test1.updated_at.isoformat().replace('+00:00', 'Z'),
            'image': f'http://testserver{test1.image.url}',
            'full_name': test1.full_name,
            'body': test1.body,
            'screenshot': f'http://testserver{test1.screenshot.url}',
            'testimony_date': str(test1.testimony_date)
        }

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(resp.content, data)

    def tearDown(self):
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except:
            pass


class UpdateTestimonyAPITest(APITestCase):

    def setUp(self) -> None:
        self.testimony = mixer.blend(Testimonies, is_deleted=False)
        self.url = reverse("api_v1:testimonies:update_testimony", args=(self.testimony.id,))
        self.user = mixer.blend('users.User', is_staff=True, is_active=True, is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.put(self.url)

        data = {'detail': 'Method "PUT" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_permission_denied(self):
        self.user.is_staff = False
        self.user.save()

        resp = self.client.post(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_not_found_testimony(self):
        self.testimony.is_deleted = True
        self.testimony.save()

        resp = self.client.patch(self.url)

        data = {'detail': 'Not found.'}

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(resp.content, data)

    def test_invalid_length_full_name(self):
        data = {
            'full_name': 'te-tee',
        }
        resp = self.client.patch(self.url, data)

        data = {
            'full_name': {
                'message': 'Please enter the correct full name, The length of the full name should at least 6 characters contains alphabets and - only'
            }
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_update_full_name_success(self):
        data = {
            'full_name': 'te t-tee',
        }
        resp = self.client.patch(self.url, data)

        data = {
            'id': self.testimony.id,
            'created_at': self.testimony.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': self.testimony.is_deleted,
            'updated_at': self.testimony.updated_at.isoformat().replace('+00:00', 'Z'),
            'image': f'http://testserver{self.testimony.image.url}',
            'full_name': 'te t-tee',
            'body': self.testimony.body,
            'screenshot': f'http://testserver{self.testimony.screenshot.url}',
            'testimony_date': str(self.testimony.testimony_date)
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_delete_testimony(self):
        data = {
            "is_deleted": True
        }

        resp = self.client.patch(self.url, data)

        data = {'message': 'successfully deleted'}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_required_at_least_one_field(self):
        resp = self.client.patch(self.url)

        data = {'message': ['you should update at least one field']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)