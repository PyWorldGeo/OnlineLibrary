from django.shortcuts import render, redirect
from .models import Book, User, Genre, Author
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, BookForm, UserForm
from .seeder import seeder_func
from django.contrib import messages
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    # seeder_func()
    # books = Book.objects.all()
    books = Book.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(genre__name__icontains=q))
    books = list(dict.fromkeys(books))
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

@login_required(login_url='login')
def adding(request, id):
    book = Book.objects.get(id=id)
    user = request.user
    user.books.add(book)
    return redirect('profile', user.id)

@login_required(login_url='login')
def delete(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        request.user.books.remove(book)
        return redirect('profile', request.user.id)

    return render(request, 'base/delete.html', {'book': book})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!")

    return render(request, 'base/login.html')


def logaut_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/register.html', context)


def add_book(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    form = BookForm()

    if request.method == "POST":
        book_author = request.POST.get('author')
        book_genre = request.POST.get('genre')

        author, created = Author.objects.get_or_create(name=book_author)
        genre, created = Genre.objects.get_or_create(name=book_genre)

        form = BookForm(request.POST)

        new_book = Book(picture=request.FILES['picture'], name=form.data['name'], author=author,
                        description=form.data['description'], file=request.FILES['file'], creator=request.user)

        if not (Book.objects.filter(file=new_book.file) or Book.objects.filter(name=new_book.name)):
            new_book.save()
            new_book.genre.add(genre)
            return redirect('home')

        return redirect('home')

    context = {'form': form, 'authors': authors, 'genres': genres}
    return render(request, 'base/add_book.html', context)


def reading(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'base/reading.html', {'book': book})


def delete_book(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.picture.delete()
        book.file.delete()
        book.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'book': book})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)

    return render(request, 'base/update_user.html', {'form': form})
