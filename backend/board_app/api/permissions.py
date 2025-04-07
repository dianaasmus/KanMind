from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from board_app.models import Board


class IsMemberOrOwner(BasePermission):
    # def has_permission(self, request, view):
    #     user = request.user
    #     if not user.is_authenticated:
    #         return False

    #     board_id = request.data.get("board")
    #     if not board_id:
    #         return False

    #     board = get_object_or_404(Board, id=board_id)

    #     return user == board.owner or board.members.filter(id=user.id).exists()

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or obj.members.filter(id=user.id).exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
