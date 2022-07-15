from django.urls import path, include

from rest_framework import routers

from sales.urls import sales_urlpatterns
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter(trailing_slash=False)

api_doc_urlpatterns = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path("dj-rest-auth/", include("dj_rest_auth.urls")),
                path("sales/", include((sales_urlpatterns, "sales"))),
                path("schema/", include(api_doc_urlpatterns)),
            ]
        ),
    )
]
