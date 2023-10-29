from django.urls import path

from tickets.views import AllTicketsView, SendAnswerView


app_name = "tickets"

urlpatterns = [
    path("tickets/", AllTicketsView.as_view(), name="all"),
    path("tickets/<int:id>/answers/", SendAnswerView.as_view(), name="answer"),
]
