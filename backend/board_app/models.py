from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class Board(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
