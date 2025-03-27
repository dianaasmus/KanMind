from django.urls import path
from .views import BoardsView, MembersView, TasksView

urlpatterns = [
    path("boards/", BoardsView.as_view()),
    path("members/", MembersView.as_view()),
    path("tasks/", TasksView.as_view()),
]
