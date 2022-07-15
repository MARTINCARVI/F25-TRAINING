from django.test import TestCase
from django.urls import reverse
from utils.tests import PrettyAssertAPITestCase, get_auth_header_for_user
from sales.fixtures import create_category_article, create_article
from users.fixtures import create_user


class BaseAuthTestMixin:
    @classmethod
    def setUpTestData(cls):

        # Create a test user:
        cls.test_user = create_user(email="user@test.com")
        cls.auth_headers = get_auth_header_for_user(cls.test_user)

        # Create a test category_article:
        cls.test_category_article = create_category_article(display_name="Cat test 2")

        # Create a test article (which belongs to the test category):
        cls.test_article = create_article(
            name="Article test 1",
            code="TST001",
            category=cls.test_category_article,
            manufacturing_cost="100",
        )

        return super().setUpTestData()


class ArticleListCreateViewTest(BaseAuthTestMixin, PrettyAssertAPITestCase):

    # TEST 1 : Test the creation of a new article
    def test_create_article(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(
            path=reverse("sales:article"),
            data={
                "name": "test2",
                "code": "TST002",
                "category": self.test_category_article.pk,
                "manufacturing_cost": "100",
            },
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["name"], "test2", response.data)

    # TEST 2 : Test the display list of articles
    def test_list_article(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        new_article = create_article(
            name="Article test 3",
            code="TST003",
            category=self.test_category_article,
            manufacturing_cost="100",
        )
        response = self.client.get(path=reverse("sales:article"))
        self.assertEqual(response.status_code, 200, response.data)
        print(response.data)
        self.assertEqual(response.data[-1]["name"], "Article test 3", response.data)
