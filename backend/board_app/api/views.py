from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from board_app.models import Board, Member, Task, Comment
from .serializers import (
    BoardListSerializer,
    MemberSerializer,
    TaskListSerializer,
    BoardDetailSerializer,
    TaskDetailSerializer,
    BoardUpdateSerializer,
    TaskUpdateSerializer,
    CommentListSerializer,
    CommentSerializer,
)


class TaskCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TaskCommentsListView(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        task = Task.objects.get(pk=pk)
        return task.comments.all()

    def create(self):
        pass


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
