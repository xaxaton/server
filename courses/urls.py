from django.urls import path

from courses.views import (
    CoursesView,
    DeleteCourseView,
    AllTestsView,
)


app_name = "courses"

urlpatterns = [
    path(
        "courses/",
        CoursesView.as_view(),
        name="all"
    ),
    path(
        "courses/<int:id>/",
        DeleteCourseView.as_view(),
        name="delete"
    ),
    path(
        "tests/",
        AllTestsView.as_view(),
        name="all-tests"
    ),
]
