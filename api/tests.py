from django.core.files.uploadedfile import SimpleUploadedFile
from mixer.backend.django import Mixer, GenFactory
from django.utils.timezone import now, timedelta
from rest_framework.test import APITestCase
from testimonies.models import Testimonies
from metal_types.models import MetalTypes
from django.urls import reverse, resolve
from favorites.models import Favorites
from locations.models import Locations
from unittest.mock import Mock, patch
from products.models import Products
from balances.models import Balances
from rest_framework import status
from knox.models import AuthToken
from django.conf import settings
from brands.models import Brands
from secrets import token_bytes
from users.models import User
from faqs.models import Faqs
from django.core import mail
from PIL import Image
from io import BytesIO
import shutil
import json
import uuid

mixer = Mixer(factory=GenFactory)


def create_file(filename='file', ext='jpg', content_type='image/jpg', size=1000, force_image=False):
    if force_image:
        img = BytesIO()
        Image.new('RGB', (100, 100)).save(img, format='JPEG')
    else:
        img = BytesIO(token_bytes(size))
    image = SimpleUploadedFile(
        f'{filename}.{ext}',
        img.getvalue(),
        content_type=content_type,

    )
    return image


def dummy_token(user, expired=None):
    return AuthToken.objects.create(user, expired)[1]


__all__ = [
    # settings
    'APITestCase',
    'Mock',
    'patch',
    'mail',
    'json',
    'mixer',
    'create_file',
    'reverse',
    'resolve',
    'status',
    'dummy_token',
    'now',
    'timedelta',
    'settings',
    'shutil',
    'uuid',

    # models
    'User',
    'Balances',
    'Brands',
    'Faqs',
    'Favorites',
    'Locations',
    'MetalTypes',
    'Products',
    'Testimonies',

]
