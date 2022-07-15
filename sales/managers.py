from django.db import models
from django.db.models import Avg, F, Sum
from django.db.models.expressions import (
    OuterRef,
    Subquery,
)


class SaleQuerySet(models.QuerySet):
    def with_revenues(self):
        return (
            self.values("article")
            .annotate(
                business_revenue=Sum(F("unit_selling_price") * F("quantity")),
                margin_percentage_per_sale=(
                    F("unit_selling_price") - F("article__manufacturing_cost")
                )
                / F("article__manufacturing_cost"),
                category_name=F("article__category__display_name"),
                pk=F("id"),
            )
            .order_by("-business_revenue")
        )


class ArticleQuerySet(models.QuerySet):
    def with_revenues(self):
        return (
            self.select_related("sale__category")
            .values("name")
            .annotate(
                business_revenue=Sum(
                    F("sales__unit_selling_price") * F("sales__quantity")
                ),
                margin_percentage_per_sale=Avg(
                    (F("sales__unit_selling_price") - F("manufacturing_cost"))
                    / F("manufacturing_cost")
                ),
                category_name=F("category__display_name"),
                pk=F("id"),
            )
            .order_by("-business_revenue")
        )

    def with_revenues_subquery(self):
        from sales.models import Sale

        sales = Subquery(
            Sale.objects.filter(article=OuterRef("pk"))
            .order_by()
            .values("article")
            .annotate(business_revenue=Sum(F("unit_selling_price") * F("quantity")))
            .values("business_revenue")
        )
        return self.annotate(business_revenue=(sales))
