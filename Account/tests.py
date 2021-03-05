from django.test import TestCase, Client
from .models import User



class ModelTest(TestCase):

    def test_user_model(self):
        user1 = User(username="Test User", email="testuser@mail.com")
        user1.set_password("test")
        user1.save()

        user = User.objects.get(email="testuser@mail.com")
        self.assertEqual(user1.username, user.username)


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        user1 = User(username="Test User", email="testuser@mail.com")
        user1.set_password("test")
        user1.save()
        
    def test_login(self):
        response = self.client.post("/login/", {"email": "testuser@mail.com", "password": "test"})
        print(response.content, end="\n\n")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post("/register/", {"username": "Test User2", "email": "testuser2@gmail.com", "password": "testuser2"})
        print(response.content, end="\n\n")
        self.assertEqual(response.status_code, 200)