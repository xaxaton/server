from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="ПрофТестиум API",
        default_version="MVP",
        description="Red Hot ОГУ Peppers",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("reviews.urls")),
    path("api/", include("courses.urls")),
]

urlpatterns += staticfiles_urlpatterns()
