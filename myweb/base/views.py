from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, User, Genre
from django.db.models import Q

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    # books = Book.objects.all()
    books = Book.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(genre__name__icontains=q))
    books = list(set(books))
    genres = Genre.objects.all()
    # print(books[0].users.all())
    heading = "Online Library"
    context = {"books": books, "heading": heading, "genres": genres}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def contact(request):
    return render(request, 'base/contact.html')


def profile(request, pk):
    user = User.objects.get(id=int(pk))

    q = request.GET.get('q') if request.GET.get('q') != None else ""

    books = user.books.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(genre__name__icontains=q))
    books = list(set(books))
    genres = Genre.objects.all()

    heading = "My Books"
    context = {'books': books, "user": user, "heading": heading, "genres": genres}
    return render(request, 'base/profile.html', context)