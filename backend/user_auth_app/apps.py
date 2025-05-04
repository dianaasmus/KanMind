from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    """
    Configuration class for the user_auth_app.

    Sets the default primary key type to BigAutoField
    and defines the app name used by Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_auth_app"
