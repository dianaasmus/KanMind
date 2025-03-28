from django.db import models


# Create your models here.
class Member(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


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
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="tasks_assign"
    )
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(Member, related_name="boards", blank=True)
    owner = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="owned_boards"
    )

    def __str__(self):
        return self.title
