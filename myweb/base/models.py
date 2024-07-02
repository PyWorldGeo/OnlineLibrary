from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET("Unknown Author"))
    picture = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, blank=True, related_name='books')
    description = models.TextField(max_length=500)
    file = models.FileField(null=True)

    def __str__(self):
        return f"{self.name} _ {self.author}"


class User(AbstractUser):
    books = models.ManyToManyField(Book, blank=True, related_name='users')