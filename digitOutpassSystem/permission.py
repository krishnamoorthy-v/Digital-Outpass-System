from rest_framework.permissions import BasePermission


class EditPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        allowed_user_ids = []
        return user.id in allowed_user_ids


class DeletePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        allowed_user_ids = []
        return user.id in allowed_user_ids


