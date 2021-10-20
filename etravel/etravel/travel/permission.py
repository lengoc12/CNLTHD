from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["get_current_user",]:
            return request.user.is_authenticated
        elif view.action in ["block_user"]:
            return request.user.is_superuser
        elif request.method in SAFE_METHODS or view.action == "create":
            return True
        return request.user.is_authenticated

