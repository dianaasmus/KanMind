from django.contrib import admin
from .models import Board, Task, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

admin.site.index_title = "KanMind - Admin Panel"


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for Django's built-in User model.
    Displays selected user fields in the user list and customizes the user creation form.
    """

    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
    )


class BoardAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Board model.
    Displays the board ID and title in the list view.
    """

    list_display = ("id", "title")


class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Task model.
    Displays task details such as ID, title, status, priority, and creator.
    """

    list_display = ("id", "title", "status", "priority", "creator")


class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Comment model.
    Displays comment ID, author, and creation timestamp.
    """

    list_display = ("id", "author", "created_at")


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
