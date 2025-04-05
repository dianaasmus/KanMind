from rest_framework import generics
from board_app.models import Board, Task, Comment
from .permissions import IsOwnerOrMember
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
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer


class BoardSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsOwnerOrMember]


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
