import shutil
import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from city_country.models import City, Country
from hiker import settings
from mainpage.models import Article, Tag
from mainpage.serializers import PostListSerializer, PostSerializer, TagSerializer
from users.models import Userc
from users.tests import Snippet

MEDIA_ROOT = tempfile.mkdtemp()
shutil.copyfile('C:/Users/1/Pictures/graphics/test.jpg', MEDIA_ROOT + r"\test.jpg")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ArticleTests(APITestCase):

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
                                           author=self.user
                                           )
        for i in range(15):
            Article.objects.create(title='1 post' + str(i),
                                   description='1post lorem1post lorem1post lorem' + str(i),
                                   content='1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem' + str(
                                       i),
                                   author=self.user
                                   )
        self.tag = Tag.objects.create(name='tag')
        for i in range(15):
            Tag.objects.create(name='tag' + str(i))

    def test_list_posts(self):
        response = self.client.get(reverse('blog'), {'search': ''})
        serializer = PostListSerializer(Article.objects.filter(title__icontains='').order_by('-id'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        i = 2
        next = response.data.get('next')
        while next is not None:
            response_child = self.client.get(next[17:])
            self.assertEqual(response_child.status_code, status.HTTP_200_OK)
            self.assertEqual(response_child.data.get('results'), serializer.data[i:i + 2])
            i = i + 2
            next = response_child.data.get('next')

    def test_list_tags(self):
        response = self.client.get(reverse('tags'), {'search': ''})
        serializer = TagSerializer(Tag.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_post(self):
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}), format='json')
        serializer = PostSerializer(Article.objects.get(slug=self.post.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_post_valid(self):
        data = {
            'title': 'post',
            'description': '1post lorem1post lorem1post lorem',
            'content': '1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem',
            'author_id': self.user.id,
        }
        response = self.client.post(reverse('create'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_invalid(self):
        data = {
            'title': 'post',
            'description': '1post lorem1post lorem1post lorem',
            'content': '1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem',
        }
        response = self.client.post(reverse('create'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_view(self):
        response = self.client.get(reverse('add_view', kwargs={'slug': self.post.slug}), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_post(self):
        data = {
            'title': 'post_edit',
            'description': '1post lorem1post lorem1post lorem',
            'content': '1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem',
            'author_id': self.user.id,
        }
        response = self.client.put(reverse('edit', kwargs={'slug': self.post.slug}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data.get('title'))

    def test_add_point(self):
        data = {
            'lng': 34.0132500,
            'lat': -6.8325500}
        response = self.client.post(reverse('add_point', kwargs={'slug': self.post.slug}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_set_points(self):
        data = {
            'lng': 34.0132500,
            'lat': -6.8325500}
        for i in range(10):
            data['lng'] = round(data.get('lng') + 1, 8)
            data['lat'] = round(data.get('lat') + 1, 8)
            r = self.client.post(reverse('add_point', kwargs={'slug': self.post.slug}), data, format='multipart')
        self.assertEqual(len(self.post.waypoints.all()), 10)
        response = self.client.post(reverse('set_points', kwargs={'slug': self.post.slug}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.post.waypoints.all()), 0)

    def test_delete_post(self):
        response = self.client.delete(reverse('delete', kwargs={'slug': self.post.slug}), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()