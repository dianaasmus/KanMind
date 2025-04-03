from django.contrib import admin
from .models import Board, Task, Comment


admin.site.index_title = "KanMind - Admin Panel"


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")


admin.site.register(Board, BoardAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
