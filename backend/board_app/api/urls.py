from django.urls import path
from .views import (
    BoardsListView,
    BoardSingleView,
    TasksListView,
    TaskSingleView,
    TaskCommentsListView,
    TaskCommentSingleView,
    AssignedTasksView,
)

urlpatterns = [
    path("boards/", BoardsListView.as_view()),
    path("boards/<int:pk>/", BoardSingleView.as_view()),
    path("tasks/", TasksListView.as_view()),
    path("tasks/<int:pk>/", TaskSingleView.as_view()),
    path("tasks/<int:pk>/comments/", TaskCommentsListView.as_view()),
    path(
        "tasks/<int:task_id>/comments/<int:pk>/",
        TaskCommentSingleView.as_view(),
    ),
    path(
        "tasks/assigned-to-me/",
        AssignedTasksView.as_view(),
        name="assigned_task",
    ),
]
