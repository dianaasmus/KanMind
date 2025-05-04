from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Represents a user profile that extends the built-in User model.

    Each UserProfile is linked to a User object and contains the user's full name.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        fullname (CharField): The full name of the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname
