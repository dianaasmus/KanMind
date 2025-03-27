from django.db import models


# Create your models here.
class Member(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class Task(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(Member, related_name="boards", blank=True)
    tasks = models.ManyToManyField(Task, related_name="boards", blank=True)

    def __str__(self):
        return self.title
