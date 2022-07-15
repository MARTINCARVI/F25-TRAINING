from pprint import pprint
from django.urls import reverse
from utils.tests import PrettyAssertAPITestCase, get_auth_header_for_user
from sales.fixtures import create_category_article, create_article, create_sale
from users.fixtures import create_user

from sales.models import Sale


class BaseAuthTestMixin:
    @classmethod
    def setUpTestData(cls):

        # Create a test user:
        cls.test_user = create_user(email="user@test.com")
        cls.auth_headers = get_auth_header_for_user(cls.test_user)

        # Create a test category_article:
        cls.category_article = create_category_article(display_name="Cat test 2")

        # Create a test article (which belongs to the test category):
        cls.article = create_article(
            name="Article test 1",
            code="TST001",
            category=cls.category_article,
            manufacturing_cost="100",
        )

        # Create a test sale:
        cls.sale = create_sale(
            author=cls.test_user,
            article=cls.article,
            quantity=None,
            unit_selling_price=None,
        )

        return super().setUpTestData()


class SaleListCreateViewTest(BaseAuthTestMixin, PrettyAssertAPITestCase):

    # TEST 1 : Test the creation of a new sale
    def test_create_sale(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(
            path=reverse("sales:sales"),
            data={
                "author": self.test_user.pk,
                "article": self.article.pk,
                "quantity": "10",
                "unit_selling_price": "200.00",
            },
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["unit_selling_price"], "200.00", response.data)

    # TEST 2 : Test the display list of all sales
    def test_list_sale(self):
        # self.client.credentials(**self.auth_headers)
        self.client.force_authenticate(user=self.test_user)
        new_article = create_sale(
            author=self.test_user,
            article=self.article,
            quantity="15",
            unit_selling_price="139.99",
        )
        response = self.client.get(path=reverse("sales:sales"))
        self.assertEqual(response.status_code, 200, response.data)
        print(response.data[0])
        self.assertEqual(Sale.objects.count(), 2)
        self.assertEqual(response.data[-1].get().unit_selling_price, "139.99")


class RetrieveUpdateDeleteSaleViewTest(BaseAuthTestMixin, PrettyAssertAPITestCase):
    pass
