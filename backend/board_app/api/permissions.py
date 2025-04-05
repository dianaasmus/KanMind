from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    def has_permission(self, request, view):  # nur für List
        if request == "POST" or "GET":
            return request.user.is_authenticated
        # if view.action in ["list", "create"]:
        #     return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):  # nur für retrive
        user = request.user
        return user == obj.owner or obj.members.filter(id=user.id).exists()


class IsMemberOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or obj.members.filter(id=user.id).exists()
