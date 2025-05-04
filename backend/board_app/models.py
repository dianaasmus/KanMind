from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Model representing a task within a board.
    A task has a creator, is assigned to a board, and may include assignees and reviewers.
    It also tracks status, priority, and a due date.
    """

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

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        help_text="User who created the task",
    )
    title = models.CharField(max_length=50, help_text="Title of the task")
    board = models.ForeignKey(
        "Board",
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Board to which the task belongs",
    )
    description = models.CharField(
        max_length=225, blank=True, null=True, help_text="Short description of the task"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="to-do",
        help_text="Current status of the task",
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default="medium",
        help_text="Priority level of the task",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        help_text="User assigned to review the task",
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_task",
        help_text="User assigned to work on the task",
    )
    due_date = models.DateField(
        null=True, blank=True, help_text="Due date for the task"
    )

    def __str__(self):
        return self.title


class Board(models.Model):
    """
    Model representing a board which groups related tasks.
    Boards have a title, an owner, and can have multiple members.
    """

    title = models.CharField(max_length=50, help_text="Title of the board")
    members = models.ManyToManyField(
        User,
        related_name="boards",
        blank=True,
        help_text="Users who are members of this board",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards",
        help_text="User who owns the board",
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model representing a comment on a task.
    Each comment has an author, content, and a timestamp of when it was created.
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Task this comment is related to",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who wrote the comment"
    )
    content = models.TextField(help_text="Text content of the comment")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Time when the comment was created"
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
