from api.tests import (
    status, APITestCase, Brands,
    reverse, create_file, mixer,
    settings, uuid
)


class ListBrandsAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:brands:list_brands")

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_list_no_brands(self):

        resp = self.client.get(self.url)

        data = {'count': 0, 'next': None, 'previous': None, 'results': []}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_list_brands_success(self):
        brand = mixer.blend(Brands)

        resp = self.client.get(self.url)

        data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': str(brand.id),
                    'created_at': brand.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': brand.is_deleted,
                    'updated_at': brand.updated_at.isoformat().replace('+00:00', 'Z'),
                    'name': brand.name
                }
            ]
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class RetrieveBrandAPITest(APITestCase):
    def setUp(self) -> None:
        self.brand = mixer.blend(Brands)
        self.url_pattern = "api_v1:brands:get_brand"
        self.url = reverse(self.url_pattern, args=(str(self.brand.id),))

        self.user = mixer.blend('users.User', is_staff=True, is_superuser=True, is_active=True)

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_brand_not_found(self):

        resp = self.client.get(reverse(self.url_pattern, args=(str(uuid.uuid4()),)))

        data = {'detail': 'Not found.'}

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(resp.content, data)

    def test_permission_denied(self):
        self.user.is_staff = False
        self.user.save()

        resp = self.client.get(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_get_brand_success(self):
        resp = self.client.get(self.url)

        data = {
            'id': str(self.brand.id),
            'created_at': self.brand.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': self.brand.is_deleted,
            'updated_at': self.brand.updated_at.isoformat().replace('+00:00', 'Z'),
            'name': self.brand.name
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)


class CreateBrandAPITest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("api_v1:brands:create_brand")
        self.user = mixer.blend('users.User', is_staff=True, is_superuser=True, is_active=True)

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_required_fields(self):

        resp = self.client.post(self.url)

        data = {'name': ['This field is required.']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_success_brand_created(self):
        data = {
            "name": "test brand"
        }

        resp = self.client.post(self.url, data)

        brand = Brands.objects.last()

        data = {
            'id': str(brand.id),
            'created_at': brand.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': brand.is_deleted,
            'updated_at': brand.updated_at.isoformat().replace('+00:00', 'Z'),
            'name': brand.name
        }

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(resp.content, data)


class UpdateBrandAPITest(APITestCase):
    def setUp(self) -> None:
        self.url_pattern = "api_v1:brands:update_brand"
        self.brand = mixer.blend(Brands)
        self.url = reverse(self.url_pattern, args=(str(self.brand.id),))
        self.user = mixer.blend('users.User', is_staff=True, is_superuser=True, is_active=True)
        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_permission_denied(self):
        self.user.is_staff = False
        self.user.save()

        resp = self.client.patch(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_required_one_field(self):
        resp = self.client.patch(self.url)

        data = {'message': ['You should update at least one field']}

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_update_name_success(self):
        data = {
            "name": "test"
        }

        resp = self.client.patch(self.url, data)
        self.brand.refresh_from_db()

        data = {
            'id': str(self.brand.id),
            'created_at': self.brand.created_at.isoformat().replace('+00:00', 'Z'),
            'is_deleted': self.brand.is_deleted,
            'updated_at': self.brand.updated_at.isoformat().replace('+00:00', 'Z'),
            'name': "test"
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)
