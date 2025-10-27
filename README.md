📚 Online Library
An interactive Django-based web application that allows users to register, upload, and read digital books, browse by genre or author, and leave comments. It also includes an example test model (Animal) to demonstrate Django’s testing framework.

🚀 Features
👤 User Authentication

Register,  login,  logout.

Update profile with avatar, bio, and favorite books.

📖 Books Management

Upload books with title, author, description, picture, and file.

Categorize books by multiple genres.

View, read, or delete books.

Add books to personal collection.

💬 Comments

Leave comments on books.

Delete comments.

🧠 Search

Search books by name, description, or genre.

🧑‍💻 Admin Panel

Manage all users, authors, books, genres, comments, and test data (Animal).

🧩 Project Structure
bash
Copy
Edit
base/
 ├── admin.py          # Admin configuration
 ├── models.py         # Database models
 ├── forms.py          # Custom user and book forms
 ├── views.py          # Application logic and routes
 ├── urls.py           # URL mappings
 ├── tests.py          # Unit tests
 ├── middleware.py     # Custom middleware example
 ├── templates/base/   # HTML templates
 └── static/           # Static files (CSS, JS, images)
⚙️ Models Overview
User: Extends Django’s AbstractUser with bio, avatar, and favorite books.

Book: Includes name, description, genre, author, file, and creator.

Author and Genre: Linked to books.

Comment: Linked to both User and Book.

Animal: Example test model (used in tests.py).

🧠 Middleware Example
NewMiddleware demonstrates how to execute logic before and after each request:

python
Copy
Edit
class NewMiddleware:
    def __call__(self, request):
        print("Before")
        response = self.get_response(request)
        print("After")
        return response
🧪 Testing Example
tests.py includes a basic Django unit test:

python
Copy
Edit
class AnimalTestCase(TestCase):
    def test_animal_can_speak(self):
        lion = Animal.objects.get(name='Lion')
        self.assertEquals(lion.speak(), 'The Lion says "Roar"')
Run tests with:

bash
Copy
Edit
python manage.py test


🖼️ Example URLs
Page	URL
Home	/
About	/about/
Contact	/contact/
Login	/login/
Register	/register/
Profile	/profile/<user_id>/
Add Book	/add/

🧰 Admin Management
Access the admin interface at /admin/ to manage:

Users

Books

Authors

Genres

Comments

Animals

🧾 License
This project is open-source and available under the MIT License.
