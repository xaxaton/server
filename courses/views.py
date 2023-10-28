from rest_framework.generics import ListAPIView

from courses.models import Tariff
from courses.serializers import TariffSerializer


class TariffView(ListAPIView):
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter()
