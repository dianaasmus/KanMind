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


class IsTaskCreatorOrBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_creator = obj.creator == request.user
        is_board_owner = obj.board.owner == request.user

        return is_creator or is_board_owner


class IsCommentMemberOrOwner(BasePermission):
    def has_permission(self, request, view):
        task_id = view.kwargs.get("pk")
        try:
            task = Task.objects.get(pk=task_id)
            board = task.board
            user = request.user

            is_board_owner = board.owner == user
            is_board_member = board.members.filter(id=user.id).exists()

            return is_board_owner or is_board_member

        except Task.DoesNotExist:
            return False


class isCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
