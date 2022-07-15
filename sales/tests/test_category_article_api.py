from django.test import TestCase
from django.urls import reverse
from utils.tests import PrettyAssertAPITestCase, get_auth_header_for_user
from sales.fixtures import create_category_article
from users.fixtures import create_user


class BaseAuthTestMixin:
    @classmethod
    def setUpTestData(cls):

        # Create a test user:
        cls.test_user = create_user(email="user@test.com")
        cls.auth_headers = get_auth_header_for_user(cls.test_user)

        # Create a test category_article:
        cls.category_article = create_category_article(display_name="Cat test 1")

        return super().setUpTestData()


class CategoryArticleListCreateViewTest(BaseAuthTestMixin, PrettyAssertAPITestCase):

    # TEST 1 : Test the creation of a new category article
    def test_create_category_article(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(
            path=reverse("sales:category"),
            data={"display_name": "test"},
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["display_name"], "test", response.data)

    # TEST 2 : Test the display list of article categories
    def test_list_category_article(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        new_category_article = create_category_article(display_name="Cat test 2")
        response = self.client.get(path=reverse("sales:category"))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data[-1]["display_name"], "Cat test 2", response.data)
