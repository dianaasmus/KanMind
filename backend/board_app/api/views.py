from rest_framework import generics
from board_app.models import Board, Task, Comment
from .serializers import (
    BoardListSerializer,
    BoardSerializer,
    TasksListSerializer,
    TaskSerializer,
    TaskCommentsListSerializer,
    TaskCommentSingleSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsStaffOrReadOnly,
    IsAdminForDeleteOrPatchAndReadOnly,
    IsAdminOrOwner,
)


class BoardsListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]


class BoardSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminOrOwner]


class TasksListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksListSerializer


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
