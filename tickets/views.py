from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsRecruiter
from tickets.models import Ticket, TicketAnswer


class AllTicketsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user:
            if request.user.role > 0:
                tickets = Ticket.objects.all()
            else:
                tickets = Ticket.object.filter(user=request.user)
            data = [
                {
                    "id": model.id,
                    "text": model.text,
                    "full_name": request.user.get_full_name(),
                    "answer": {
                        "id": TicketAnswer.objects.get(ticket=model).id,
                        "text": TicketAnswer.objects.get(ticket=model).text,
                    }
                    if TicketAnswer.objects.filter(ticket=model)
                    else None,
                }
                for model in tickets
            ]
            return Response(data)
        else:
            return Response([])

    def post(self, request, *args, **kwargs):
        text = request.data.get("text", None)
        user = request.user
        new_ticket = Ticket.objects.create(text=text, user=user)
        return Response({"ticket": model_to_dict(new_ticket)})


class SendAnswerView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsRecruiter,
    )

    def post(self, request, id, *args, **kwargs):
        text = request.data.get("text", None)
        ticket = Ticket.objects.get(id=id)
        new_answer = TicketAnswer.objects.create(
            text=text,
            ticket=ticket,
        )
        return Response(model_to_dict(new_answer))
