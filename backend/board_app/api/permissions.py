from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from board_app.models import Board, Task
from rest_framework.exceptions import AuthenticationFailed


class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, Task):
            board = obj.board
            return board.members.filter(id=user.id).exists()
        else:
            return obj.members.filter(id=user.id).exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        else:
            raise AuthenticationFailed(
                "You must be the owner of this board to perform this action."
            )
