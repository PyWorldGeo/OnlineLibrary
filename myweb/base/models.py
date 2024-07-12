from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now



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
    creator = models.ForeignKey('User', on_delete=models.SET("Unknown Creator"))
    author = models.ForeignKey(Author, on_delete=models.SET("Unknown Author"))
    picture = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, blank=True, related_name='books')
    description = models.TextField(max_length=500)
    file = models.FileField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class User(AbstractUser):
    books = models.ManyToManyField(Book, blank=True, related_name='users')
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body

