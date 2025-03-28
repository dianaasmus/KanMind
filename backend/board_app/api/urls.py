from django.urls import path, include
from .views import MembersView, TasksViewSet, BoardsViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"boards", BoardsViewSet)
router.register(r"tasks", TasksViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("boards/", BoardsView.as_view()),
    path("members/", MembersView.as_view()),
    # path("tasks/", TasksView.as_view()),
]
