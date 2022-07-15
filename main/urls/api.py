from django.urls import path, include

from rest_framework import routers

from sales.urls import sales_urlpatterns

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path("dj-rest-auth/", include("dj_rest_auth.urls")),
                path("sales/", include((sales_urlpatterns, "sales"))),
            ]
        ),
    )
]
