from django.urls import path, include
from .views import (
    # MembersView,
    # TasksViewSet,
    # BoardsViewSet,
    # TaskCommentsListView,
    # TaskCommentDetailView,
    BoardsListView,
    BoardSingleView,
    # TasksListView,
    # TaskSingleView,
    # TaskCommentsListView,
    # TaskCommentSingleView,
    # MembersListView,
)
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r"boards", BoardsViewSet)
# router.register(r"tasks", TasksViewSet)


# urlpatterns = [
#     path("", include(router.urls)),
#     # path("boards/", BoardsView.as_view()),
#     path("members/", MembersView.as_view()),
#     # path("tasks/", TasksView.as_view()),
#     path("tasks/<int:pk>/comments/", TaskCommentsListView.as_view()),
#     path("tasks/<int:pk>/comments/<int:comment_id>/", TaskCommentDetailView.as_view()),
# ]

urlpatterns = [
    path("boards/", BoardsListView.as_view()),
    path("boards/<int:pk>/", BoardSingleView.as_view()),
    # path("tasks/", TasksListView.as_view()),
    # path("tasks/<int:pk>/", TaskSingleView.as_view()),
    # path("tasks/<int:pk>/comments/", TaskCommentsListView.as_view()),
    # path(
    #     "tasks/<int:task_id>/comments/<int:comment_id>/", TaskCommentSingleView.as_view()
    # ),
    # path("members/", MembersListView.as_view()),
]
