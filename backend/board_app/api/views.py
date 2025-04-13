from rest_framework import generics, status
from board_app.models import Board, Task, Comment

from .permissions import (
    IsMember,
    IsOwner,
    IsTaskCreatorOrBoardOwner,
    IsCommentMemberOrOwner,
    isCreator,
    IsOwnerOrMember,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response


from .serializers import (
    BoardListSerializer,
    BoardSerializer,
    TasksListSerializer,
    TaskSerializer,
    TaskCommentsListSerializer,
    TaskCommentSingleSerializer,
)


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TasksListSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class BoardsListView(generics.ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, IsMember, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user) | Board.objects.filter(members=user)


class BoardSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsOwner()]
        elif self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsOwnerOrMember()]
        else:
            return [IsAuthenticated(), IsMember()]


class TasksListView(generics.ListCreateAPIView):
    serializer_class = TasksListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(board__owner=user) | Task.objects.filter(
            board__members=user
        )


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        else:
            return [IsAuthenticated(), IsMember()]


class TaskCommentsListView(generics.ListCreateAPIView):
    serializer_class = TaskCommentsListSerializer
    permission_classes = [IsAuthenticated, IsCommentMemberOrOwner]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        task = Task.objects.get(pk=pk)
        return task.comments.all()


class TaskCommentSingleView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskCommentSingleSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAuthenticated, isCreator]


class EmailCheckView(APIView):
    def get(self, request):
        email = request.query_params.get("email")

        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "fullname": f"{user.first_name} {user.last_name}",
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ReviewingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasksListSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)
