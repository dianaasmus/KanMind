from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from board_app.models import Board, Task
from rest_framework.exceptions import AuthenticationFailed


class IsMember(BasePermission):
    """
    Allows access only to members of the board.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a member of the board related to the object.
        """
        user = request.user
        if isinstance(obj, Task):
            board = obj.board
            return board.members.filter(id=user.id).exists()
        else:
            return obj.members.filter(id=user.id).exists()


class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the object.
        """
        return request.user == obj.owner


class IsOwnerOrMember(BasePermission):
    """
    Allows access if the user is either the owner or a member of the board.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is either a board member or the board owner.
        """
        is_member = IsMember().has_object_permission(request, view, obj)
        is_owner = IsOwner().has_object_permission(request, view, obj)
        return is_member or is_owner


class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Allows access to the creator of the task or the owner of the board.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user created the task or owns the board.
        """
        is_creator = obj.creator == request.user
        is_board_owner = obj.board.owner == request.user
        return is_creator or is_board_owner


class IsCommentMemberOrOwner(BasePermission):
    """
    Allows access to members or the owner of the board related to a comment's task.
    """

    def has_permission(self, request, view):
        """
        Check if the user is a member or owner of the board related to the task.
        """
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
    """
    Allows access only to the creator (author) of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the author of the object.
        """
        return obj.author == request.user
