from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from board_app.models import Board, Member, Task
from .serializers import (
    BoardListSerializer,
    MemberSerializer,
    TaskSerializer,
    BoardDetailSerializer,
)


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        return BoardListSerializer


class MembersView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
