from django.contrib import admin
from .models import Board, Member, Task


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "fullname",
    )


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority")


admin.site.register(Board, BoardAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Task, TaskAdmin)
