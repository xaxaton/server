from django.forms.models import model_to_dict

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(is_published=True)

    def post(self, request, *args, **kwargs):
        video = request.data["review"].get("video", None)
        image = request.data["review"].get("image", None)
        if video == "":
            video = None
        if image == "":
            image = None
        review = Review.objects.create(
            text=request.data["review"]["text"],
            video=video,
            image=image,
        )
        return Response({"review": model_to_dict(review)})
