from api.tests import (
    mixer, Balances, dummy_token,
    status, APITestCase, reverse,
    create_file, shutil, settings
)


class TestListBalancesAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend('users.User', is_email_verified=True)
        self.url = reverse("api_v1:balances:list_balances")

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_email_not_verified(self):
        self.user.is_email_verified = False
        self.user.save()

        resp = self.client.get(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_list_no_balances(self):
        mixer.blend(Balances)
        resp = self.client.get(self.url)

        data = {'count': 0, 'next': None, 'previous': None, 'results': []}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_list_balances(self):
        balance = mixer.blend(Balances, user=self.user)

        resp = self.client.get(self.url)

        data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': balance.id.__str__(),
                    'purchase_date':  balance.purchase_date.isoformat().replace('+00:00', 'Z'),
                    'purchase_price':balance.purchase_price,
                    'gm_price':balance.gm_price,
                    'packing_per_gm': balance.packing_per_gm,
                    'cashback_per_gm': balance.cashback_per_gm,
                    'is_available': balance.is_available,
                    'bill_scan': f"http://testserver{balance.bill_scan.url}",
                    'product': {
                        'id': balance.product.id.__str__(),
                        'created_at': balance.product.created_at.isoformat().replace('+00:00', 'Z'),
                        'is_deleted': balance.product.is_deleted,
                        'updated_at':  balance.product.updated_at.isoformat().replace('+00:00', 'Z'),
                        'title': balance.product.title,
                        'description': balance.product.description,
                        'weight': balance.product.weight,
                        'kirat': balance.product.kirat,
                        'fitness': balance.product.fitness,
                        'is_available': balance.product.is_available,
                        'brand': {
                            'id': balance.product.brand.id.__str__(),
                            'created_at': balance.product.brand.created_at.isoformat().replace('+00:00', 'Z'),
                            'is_deleted': balance.product.brand.is_deleted,
                            'updated_at': balance.product.brand.updated_at.isoformat().replace('+00:00', 'Z'),
                            'name': balance.product.brand.name
                        },
                        'metal_type': {
                            'id': balance.product.metal_type.id.__str__(),
                            'created_at':  balance.product.metal_type.created_at.isoformat().replace('+00:00', 'Z'),
                            'is_deleted': balance.product.metal_type.is_deleted,
                            'name': balance.product.metal_type.name
                        }
                    }
                }
            ]
        }
        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def tearDown(self):
        # Remove uploaded images
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except:
            pass


class GetBalanceAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend('users.User', is_email_verified=True)
        self.balance = mixer.blend(Balances, user_id= self.user.id)
        self.url = reverse("api_v1:balances:get_balance", args=(str(self.balance.id),))

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.post(self.url)

        data = {'detail': 'Method "POST" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_email_not_verified(self):
        self.user.is_email_verified = False
        self.user.save()

        resp = self.client.get(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_get_balance(self):

        resp = self.client.get(self.url)

        data = {
            'id': self.balance.id.__str__(),
            'purchase_date': self.balance.purchase_date.isoformat().replace('+00:00', 'Z'),
            'purchase_price': self.balance.purchase_price,
            'gm_price': self.balance.gm_price,
            'packing_per_gm': self.balance.packing_per_gm,
            'cashback_per_gm': self.balance.cashback_per_gm,
            'is_available': self.balance.is_available,
            'bill_scan': f"http://testserver{self.balance.bill_scan.url}",
            'product': {
                'id': self.balance.product.id.__str__(),
                'created_at': self.balance.product.created_at.isoformat().replace('+00:00', 'Z'),
                'is_deleted': self.balance.product.is_deleted,
                'updated_at': self.balance.product.updated_at.isoformat().replace('+00:00', 'Z'),
                'title': self.balance.product.title,
                'description': self.balance.product.description,
                'weight': self.balance.product.weight,
                'kirat': self.balance.product.kirat,
                'fitness': self.balance.product.fitness,
                'is_available': self.balance.product.is_available,
                'brand': {
                    'id': self.balance.product.brand.id.__str__(),
                    'created_at': self.balance.product.brand.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': self.balance.product.brand.is_deleted,
                    'updated_at': self.balance.product.brand.updated_at.isoformat().replace('+00:00', 'Z'),
                    'name': self.balance.product.brand.name
                },
                'metal_type': {
                    'id': self.balance.product.metal_type.id.__str__(),
                    'created_at': self.balance.product.metal_type.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': self.balance.product.metal_type.is_deleted,
                    'name': self.balance.product.metal_type.name
                }
            }
        }

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def test_not_found_balance(self):
        u = mixer.blend("users.User")
        self.balance.user = u
        self.balance.save()

        resp = self.client.get(self.url)

        data = {'detail': 'Not found.'}

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(resp.content, data)

    def tearDown(self):
        # Remove uploaded images
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except:
            pass


class CreateBalanceAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend("users.User", is_email_verified=True)
        self.url = reverse("api_v1:balances:create_balance")

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_email_not_verified(self):
        self.user.is_email_verified = False
        self.user.save()

        resp = self.client.get(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_required_fields(self):
        resp = self.client.post(self.url)

        data = {
            'purchase_date': ['This field is required.'],
            'purchase_price': ['This field is required.'],
            'gm_price': ['This field is required.'],
            'packing_per_gm': ['This field is required.'],
            'cashback_per_gm': ['This field is required.'],
            'bill_scan': ['No file was submitted.'],
            'product': ['This field is required.']
        }

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(resp.content, data)

    def test_create_success(self):
        prod = mixer.blend('products.Products')
        data = {
            'purchase_date': "2023-03-02",
            'purchase_price': 20.0,
            'gm_price': 10,
            'packing_per_gm': 12,
            'cashback_per_gm': 13,
            'bill_scan': create_file(force_image=True),
            'product': str(prod.id)
        }

        resp = self.client.post(self.url, data)

        balance = Balances.objects.last()

        data = {
            'id': balance.id.__str__(),
            'purchase_date': balance.purchase_date.isoformat().replace('+00:00', 'Z'),
            'purchase_price': balance.purchase_price,
            'gm_price': balance.gm_price,
            'packing_per_gm': balance.packing_per_gm,
            'cashback_per_gm': balance.cashback_per_gm,
            'is_available': balance.is_available,
            'bill_scan': f"http://testserver{balance.bill_scan.url}",
            'product': {
                'id': prod.id.__str__(),
                'created_at': prod.created_at.isoformat().replace('+00:00', 'Z'),
                'is_deleted': prod.is_deleted,
                'updated_at': prod.updated_at.isoformat().replace('+00:00', 'Z'),
                'title': prod.title,
                'description': prod.description,
                'weight': prod.weight,
                'kirat': prod.kirat,
                'fitness': prod.fitness,
                'is_available': prod.is_available,
                'brand': {
                    'id': prod.brand.id.__str__(),
                    'created_at': prod.brand.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': prod.brand.is_deleted,
                    'updated_at': prod.brand.updated_at.isoformat().replace('+00:00', 'Z'),
                    'name': prod.brand.name
                },
                'metal_type': {
                    'id': prod.metal_type.id.__str__(),
                    'created_at': prod.metal_type.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': prod.metal_type.is_deleted,
                    'name': prod.metal_type.name
                }
            }
        }

        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(resp.content, data)

    def tearDown(self):
        # Remove uploaded images
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except:
            pass


class UpdateBalanceAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = mixer.blend('users.User', is_email_verified=True)
        self.balance = mixer.blend(Balances, user_id=self.user.id)
        self.url = reverse("api_v1:balances:update_balance", args=(str(self.balance.id), ))

        self.client.force_authenticate(self.user)

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)

        data = {'detail': 'Method "GET" not allowed.'}

        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertJSONEqual(resp.content, data)

    def test_email_not_verified(self):
        self.user.is_email_verified = False
        self.user.save()

        resp = self.client.get(self.url)

        data = {'detail': 'You do not have permission to perform this action.'}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(resp.content, data)

    def test_no_balance_found(self):
        u = mixer.blend('users.User')
        self.balance.user = u
        self.balance.save()

        resp = self.client.patch(self.url)

        data = {'detail': 'Not found.'}

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(resp.content, data)

    def test_update_bill_scan_success(self):
        data = {
            'bill_scan': create_file(force_image=True)
        }

        resp = self.client.patch(self.url, data)

        self.balance.refresh_from_db()

        data = data = {
            'id': self.balance.id.__str__(),
            'purchase_date': self.balance.purchase_date.isoformat().replace('+00:00', 'Z'),
            'purchase_price': self.balance.purchase_price,
            'gm_price': self.balance.gm_price,
            'packing_per_gm': self.balance.packing_per_gm,
            'cashback_per_gm': self.balance.cashback_per_gm,
            'is_available': self.balance.is_available,
            'bill_scan': f"http://testserver{self.balance.bill_scan.url}",
            'product': {
                'id': self.balance.product.id.__str__(),
                'created_at': self.balance.product.created_at.isoformat().replace('+00:00', 'Z'),
                'is_deleted': self.balance.product.is_deleted,
                'updated_at': self.balance.product.updated_at.isoformat().replace('+00:00', 'Z'),
                'title': self.balance.product.title,
                'description': self.balance.product.description,
                'weight': self.balance.product.weight,
                'kirat': self.balance.product.kirat,
                'fitness': self.balance.product.fitness,
                'is_available': self.balance.product.is_available,
                'brand': {
                    'id': self.balance.product.brand.id.__str__(),
                    'created_at': self.balance.product.brand.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': self.balance.product.brand.is_deleted,
                    'updated_at': self.balance.product.brand.updated_at.isoformat().replace('+00:00', 'Z'),
                    'name': self.balance.product.brand.name
                },
                'metal_type': {
                    'id': self.balance.product.metal_type.id.__str__(),
                    'created_at': self.balance.product.metal_type.created_at.isoformat().replace('+00:00', 'Z'),
                    'is_deleted': self.balance.product.metal_type.is_deleted,
                    'name': self.balance.product.metal_type.name
                }
            }
        }

        self.maxDiff = None
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, data)

    def tearDown(self):
        # Remove uploaded images
        try:
            shutil.rmtree(settings.MEDIA_ROOT)
        except:
            pass
