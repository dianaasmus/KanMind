from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("done", "Done"),
        ("review", "Review"),
    ]
    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    title = models.CharField(max_length=50)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=225)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(
        max_length=50, choices=PRIORITY_CHOICES, default="medium"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_task",
    )
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="boards", blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_boards"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
