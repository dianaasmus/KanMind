from django.contrib import admin
from .models import Board, Task, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

admin.site.index_title = "KanMind - Admin Panel"


class CustomUserAdmin(UserAdmin):
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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "creator")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
