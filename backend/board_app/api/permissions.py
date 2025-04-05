from rest_framework import permissions


class IsOwnerOrMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request == "POST":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or obj.members.filter(id=user.id).exists()
