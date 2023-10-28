from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    video = serializers.CharField(required=False)
    image = serializers.CharField(required=False)

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        return Review.objects.create(**validated_data)
