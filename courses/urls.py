from django.urls import path

from courses.views import TariffView


app_name = "courses"

urlpatterns = [
    path("tariffs/", TariffView.as_view(), name="tariffs"),
]
