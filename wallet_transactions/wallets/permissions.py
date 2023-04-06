from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    """check permissions is this user is owner"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
