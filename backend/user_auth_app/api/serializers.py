from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    Serializes all fields of the user profile.
    """

    class Meta:
        model = UserProfile
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Includes validation to ensure that passwords match and enforces unique email addresses.
    """

    repeated_password = serializers.CharField(
        write_only=True, help_text="Repeat the password for confirmation."
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="User email. Must be unique.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password"]
        extra_kwargs = {"password": {"write_only": True, "help_text": "User password"}}

    def save(self):
        """
        Creates and returns a new User instance if the passwords match.
        Raises a ValidationError if they do not.
        """
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "Passwords do not match!"})

        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        account.set_password(pw)
        account.save()
        return account
