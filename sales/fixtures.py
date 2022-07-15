from sales.models import ArticleCategory, Article, Sale
from faker import Faker

fake = Faker()


def create_category_article(*, display_name=None):
    return ArticleCategory.objects.create(display_name=display_name or fake.name())


def create_article(*, name=None, code=None, category=None, manufacturing_cost=None):
    return Article.objects.create(
        name=name or fake.name(),
        code=code,
        category=category,
        manufacturing_cost=manufacturing_cost,
    )


def create_sale(
    *, date=None, author=None, article=None, quantity=None, unit_selling_price=None
):
    return Sale.objects.create(
        date=date or fake.date(),
        author=author,
        article=article,
        quantity=quantity or fake.pyint(min_value=0),
        unit_selling_price=unit_selling_price or fake.pyint(min_value=0),
    )
