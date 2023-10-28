from django.urls import path

from reviews.views import ReviewsView


app_name = "reviews"

urlpatterns = [
    path("reviews/", ReviewsView.as_view(), name="all"),
]
