from django.urls import path

from courses.views import CoursesView


app_name = "courses"

urlpatterns = [
    path(
        "courses/",
        CoursesView.as_view(),
        name="all"
    )
]
