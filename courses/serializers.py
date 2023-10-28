from rest_framework import serializers

from courses.models import Tariff


class TariffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    price = serializers.IntegerField()
    users_count = serializers.IntegerField()
    tests_count = serializers.IntegerField()

    class Meta:
        model = Tariff
        fields = "__all__"
