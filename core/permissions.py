from rest_framework import permissions


class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, views):
        return request.user.role > 0 and request.user.organization is not None
