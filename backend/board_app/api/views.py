from rest_framework import generics
from board_app.models import Board, Task, Comment
from .permissions import IsMemberOrOwner, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import (
    BoardListSerializer,
    BoardSerializer,
    TasksListSerializer,
    TaskSerializer,
    TaskCommentsListSerializer,
    TaskCommentSingleSerializer,
)


class AssignedTasksView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksListSerializer


class BoardsListView(generics.ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, IsMemberOrOwner]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user) | Board.objects.filter(members=user)


class BoardSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated(), IsMemberOrOwner()]


class TasksListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksListSerializer
    permission_classes = [IsAuthenticated, IsMemberOrOwner]

    # def get_permissions(self):
    #     if self.request.method == "POST":
    #         return [IsAuthenticated(), IsOwner()]
    #     return [IsAuthenticated(), IsMemberOrOwner()]


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCommentsListView(generics.ListCreateAPIView):
    serializer_class = TaskCommentsListSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        task = Task.objects.get(pk=pk)
        return task.comments.all()


class TaskCommentSingleView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskCommentSingleSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = "task_id"


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
