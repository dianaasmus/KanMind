from django.apps import AppConfig


class BoardConfig(AppConfig):
    """
    Configuration class for the 'board_app' Django application.
    Sets the default primary key field type and the app's name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "board_app"
