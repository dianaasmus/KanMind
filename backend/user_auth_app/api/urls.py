from django.urls import path
from .views import RegistrationView, CustomLoginView, EmailCheckView

urlpatterns = [
    path("registration/", RegistrationView.as_view()),
    path("login/", CustomLoginView.as_view()),
    path("email-check/", EmailCheckView.as_view()),
]
