from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from courses.models import Course
from courses.serializers import CourseSerializer
from users.models import Organization


class CoursesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        orgid = self.request.user.organization.id
        organization = Organization.objects.get(id=orgid)
        qs = Course.objects.filter(
            organization=organization, department=None, position=None
        )
        if self.request.user.role == 0:
            if self.request.user.department:
                department_qs = Course.objects.filter(
                    department=self.request.user.department
                )
            if self.request.user.position and self.request.user.department:
                position_qs = department_qs.filter(
                    department=self.request.user.department
                )
                qs += position_qs
        data = [
            CourseSerializer(model).data
            for model in qs
        ]
        return Response(data)

    def delete(self):
        ...
    # def post(self, request):
    #     name = request.data.get("name", None)
    #     orgid = request.data["organization"].get("id", None)
    #     organization = Organization.objects.get(id=orgid)
    #     qs = Course.objects.filter(organization=organization)
    #     if "department" in request.data:
    #         qs = qs.filter(department=request.data.get("department"))
    #     if "position" in request.data:
    #         qs = qs.filter(position=request.data.get("department"))
