from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from board_app.models import Board, Member, Task
from .serializers import (
    BoardListSerializer,
    MemberSerializer,
    TaskListSerializer,
    BoardDetailSerializer,
    TaskDetailSerializer,
    BoardUpdateSerializer,
    TaskUpdateSerializer,
)


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BoardListSerializer
        elif self.action in ["update", "partial_update"]:
            return BoardUpdateSerializer
        return BoardDetailSerializer


class MembersView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return TaskUpdateSerializer
        return TaskListSerializer

    def get_serializer_context(self):
        """Stellt sicher, dass der Request an den Serializer übergeben wird"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
