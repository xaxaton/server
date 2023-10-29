from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from courses.models import Course
from courses.serializers import CourseSerializer
from core.permissions import IsRecruiter
from users.models import Organization, Position, Department


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

    def post(self, request):
        if request.user.role > 0:
            name = request.data.get("name", None)
            orgid = request.data["organization"].get("id", None)
            dep = request.data.get("department", None)
            pos = request.data.get("position", None)
            department = None
            position = None
            if dep:
                if dep.get("id", None):
                    depid = dep.get("id", None)
                    department = Department.objects.get(id=depid)
            if pos:
                if pos.get("id", None):
                    posid = pos.get("id", None)
                    position = Position.objects.get(id=posid)

            organization = Organization.objects.get(id=orgid)
            new_course = Course.objects.create(
                name=name, organization=organization,
                department=department, position=position
            )
            return Response({
                "name": new_course.name,
                "id": new_course.id
            })
        return Response(status=status.HTTP_403_FORBIDDEN)


class DeleteCourseView(APIView):
    permission_classes = (IsAuthenticated, IsRecruiter)

    def get(self, request, id):
        Course.objects.get(id=id)
        return Response(status=status.HTTP_200_OK)
