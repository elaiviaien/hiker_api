import shutil
import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hiker import settings
from mainpage.models import Article
from users.models import Userc
from users.tests import Snippet

MEDIA_ROOT = tempfile.mkdtemp()
shutil.copyfile('/graphics/test.jpg', MEDIA_ROOT + r"\test.jpg")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ContactsTests(APITestCase):
    def setUp(self):
        settings.MEDIA_ROOT = MEDIA_ROOT

        self.data = {
            'register_url': "/auth/users/",
            'activate_url': "/auth/users/activation/",
            'login_url': "/auth/jwt/create",
            'user_details_url': "/auth/users/me/",
            'user_data': {
                "email": "test@example.com",
                "username": "test_user",
                "password": "verysecret"
            },
            'login_data': {
                "email": "test@example.com",
                "password": "verysecret"
            }, }

        self.user = Userc.objects.get(email=Snippet.register_with_email_verification(self, self.data).get('email'))
        self.post = Article.objects.create(title='1 post',
                                           description='1post lorem1post lorem1post lorem',
                                           content='1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem',
                                           author= self.user
                                           )
        self.data = {'id': self.user.id}

    def test_like(self):
        response = self.client.post(reverse('like', kwargs={'pk': self.post.id}), self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unlike(self):
        self.client.post(reverse('like', kwargs={'pk': self.post.id}), self.data)
        response = self.client.post(reverse('unlike', kwargs={'pk': self.post.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()