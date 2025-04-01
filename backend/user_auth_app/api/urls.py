from django.urls import path
from .views import UserProfileSingleView, UserProfileList, RegistrationView

urlpatterns = [
    path("profiles/", UserProfileList.as_view()),
    path("profiles/<int:pk>/", UserProfileSingleView.as_view()),
    path("registration/", RegistrationView.as_view()),
]
