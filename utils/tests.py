import logging
from contextlib import contextmanager
from io import BytesIO
import sys
from unittest.mock import patch

from django.conf import settings
from django.db.models.enums import ChoicesMeta
from django.test.runner import DiscoverRunner
from faker import Faker
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework_simplejwt.tokens import RefreshToken


fake = Faker()


class FastTestRunner(DiscoverRunner):
    """Global settings overrides to speed tests up"""

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        settings.TEMPLATE_DEBUG = False
        settings.PASSWORD_HASHERS = [
            "django.contrib.auth.hashers.MD5PasswordHasher",
        ]
        logging.disable(logging.WARNING)


class PrettyAssertAPITestCase(APITestCase):
    """Replaces OrderedDict by regular dicts in API tests responses"""

    maxDiff = None

    def _formatMessage(self, msg, standardMsg):
        if isinstance(msg, ReturnList) or isinstance(msg, ReturnDict):
            msg = api_response_to_dict(msg)
        return super()._formatMessage(msg, standardMsg)


def get_jpg_file_content():
    """Returns the binary content of a dummy JPG file of 1 pixel"""
    with open("data/1px.jpg", "rb") as f:
        return BytesIO(f.read())


@contextmanager
def image_field_validation_disabled():
    """Disables the ImageField validation"""
    mocked_validation = patch("django.forms.fields.ImageField.run_validators").start()
    mocked_validation.return_value = None
    try:
        yield
    finally:
        mocked_validation.stop()


@contextmanager
def image_cache_generation_disabled():
    """Disables the cached image generation"""
    mocked_generate = patch("imagekit.cachefiles.ImageCacheFile.generate").start()
    try:
        yield
    finally:
        mocked_generate.stop()


@contextmanager
def disable_logging(log_level):
    """Temporarily disable logging to speed tests up"""
    initial_level = logging.root.getEffectiveLevel()
    logging.disable(log_level)
    try:
        yield
    finally:
        logging.root.setLevel(initial_level)


def random_choice(choices):
    """Returns a random value from a model choices"""
    if isinstance(choices, ChoicesMeta):
        return fake.random_element(c.value for c in choices)
    else:  # Legacy tuple choices
        return fake.random_element(val for val, _ in choices)


def random_sample(*, elements, min_number=1, max_number=3):
    """Returns a random list of a random number of values (without repetition)"""
    return fake.random_sample(
        elements, length=fake.random_int(min=min_number, max=max_number)
    )


def api_response_to_dict(response_data):
    """
    APITestCase responses lists are OrderedDict that do not print nicely in the
    console. This function turns them into regular lists/dicts that can be nicely
    printed.
    """
    if isinstance(response_data, list):
        return [api_response_to_dict(el) for el in response_data]
    if isinstance(response_data, dict):
        out = {}
        for key, value in response_data.items():
            if isinstance(value, list) or isinstance(value, dict):
                out[key] = api_response_to_dict(value)
            else:
                out[key] = value
        return out
    if isinstance(response_data, ErrorDetail):
        return str(response_data)


def get_auth_header_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
