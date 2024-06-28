from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, User, Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

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


def adding(request, id):
    book = Book.objects.get(id=id)
    user = request.user
    user.books.add(book)
    return redirect('profile', user.id)


def delete(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        request.user.books.remove(book)
        return redirect('profile', request.user.id)

    return render(request, 'base/delete.html', {'book': book})


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()

        try:
            user = User.objects.get(username=username)
        except:
            pass # Error Message

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass # Error Message



    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logaut_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    context = {}
    return render(request, 'base/login_register.html', context)