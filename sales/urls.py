from django.urls import path


from sales.api_views import (
    ArticleListAgregatedView,
    ArticleListCreateView,
    SaleListCreateView,
    CategoryArticleListCreateView,
    RetrieveUpdateDeleteSaleView,
    SaleListAgregatedView,
)


sales_urlpatterns = [
    path("categories", CategoryArticleListCreateView.as_view(), name="category"),
    path("articles", ArticleListCreateView.as_view(), name="article"),
    path("", SaleListCreateView.as_view(), name="sales"),
    path(
        "<int:pk>",
        RetrieveUpdateDeleteSaleView.as_view(),
        name="retrieve_update_delete_sales",
    ),
    path(
        "revenue",
        SaleListAgregatedView.as_view(),
        name="sales_revenues",
    ),
    path("money", ArticleListAgregatedView.as_view(), name="articles_revenues"),
]
