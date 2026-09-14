from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "You must be the owner of this object to perform this action."

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user