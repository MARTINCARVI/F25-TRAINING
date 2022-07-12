from django.urls import path, include

from rest_framework import routers

from sales.api_views import (
    ArticleListView,
    SaleCreateView,
    SaleListAllView,
    SaleListAuthorView,
    CategoryArticleCreateView,
    RetrieveUpdateDeleteSaleView,
    SaleListAgregatedView,
)

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path("dj-rest-auth/", include("dj_rest_auth.urls")),
                path(
                    "categories", CategoryArticleCreateView.as_view(), name="category"
                ),
                path("articles", ArticleListView.as_view(), name="article"),
                path("all-sales/list", SaleListAllView.as_view(), name="all_sales"),
                path(
                    "author-sales/list",
                    SaleListAuthorView.as_view(),
                    name="author_sales",
                ),
                path(
                    "agregated-sales/list",
                    SaleListAgregatedView.as_view(),
                    name="author_sales",
                ),
                path("sales/add", SaleCreateView.as_view(), name="author_sales"),
                path(
                    "sales/<int:pk>",
                    RetrieveUpdateDeleteSaleView.as_view(),
                    name="retrieve_update_delete_sales",
                ),
            ]
        ),
    )
]
