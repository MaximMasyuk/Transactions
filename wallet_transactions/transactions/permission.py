from rest_framework import permissions


class IsOwnerTransaction(permissions.IsAuthenticated):
    """check permissions is this user is owner"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.sender.owner == request.user or obj.receiver.owner == request.user:
            return True
        return False
