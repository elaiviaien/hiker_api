import random
import shutil
import tempfile
from io import BytesIO

import faker
from django.core.files import File

from PIL import Image
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from city_country.models import Country, City
from hiker import settings
from mainpage.models import Article, Tag
from users.models import Region, Userc
from users.serializers import RegionSerializer, UserProfileSerializer

MEDIA_ROOT = tempfile.mkdtemp()
shutil.copyfile('C:/Users/1/Pictures/graphics/test.jpg', MEDIA_ROOT+r"\test.jpg")
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class Snippet(APITestCase):
    def register_with_email_verification(self, data_u):
        # register the new user
        response = self.client.post(data_u.get('register_url'), data_u.get('user_data'), format="json")
        # expected response

        if response.status_code == 400:
            print(MEDIA_ROOT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        # self.assertEqual(len(mail.outbox), 1)

        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        # you can print email to check it
        # print(mail.outbox[0].subject)
        # print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link[:-1].split("/")[-2:]
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(data_u.get('activate_url'), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(data_u.get('login_url'), data_u.get('login_data'), format="json")
        self.assertTrue("access" in response.json())
        token = response.json()["access"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # get user details
        response = self.client.get(data_u.get('user_details_url'), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], data_u.get('user_data')["email"])
        self.assertEqual(response.data["username"], data_u.get('user_data')["username"])
        mail.outbox = []
        return response.data

    def create_full_user(self, data_u):
        fake = Faker(['ru_RU',])
        i = random.randint(1, 348)
        img = Image.open('images/avs/' + str(i)+'.jpg').convert('RGB')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        img.save(tmp_file)
        tmp_file.seek(0)

        user = Userc.objects.get(slug=Snippet.register_with_email_verification(self, data_u).get('slug'))
        id = user.id
        data_u['user_data'].update({
            "first_name": fake.name().split(" ")[0],
            "bio": fake.text(),
            "profile_img": tmp_file
        })
        response = self.client.put(reverse('profile_edit', kwargs={'slug': user.slug}), data_u['user_data'],
                                   format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('bio'), data_u['user_data'].get('bio'))
        return id

    def follow_unfollow(self):
        user1 = Userc.objects.get(email=Snippet.register_with_email_verification(self, self.data).get('email'))
        data = {
            'register_url': "/auth/users/",
            'activate_url': "/auth/users/activation/",
            'login_url': "/auth/jwt/create",
            'user_details_url': "/auth/users/me/",
            'user_data': {
                "email": "test@example.com1",
                "username": "test_user1",
                "password": "verysecret1",
            },
            'login_data': {
                "email": "test@example.com1",
                "password": "verysecret1"
            },
        }

        user2 = Userc.objects.get(email=Snippet.register_with_email_verification(self, data).get('email'))
        response = self.client.post(reverse('follow', kwargs={'pk': user1.id}), {'id': user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get("followers")), 1)
        return user1, user2
    def auto_user(self):
        fake = Faker(['ru_RU', ])
        country = fake.country()
        # creating countries
        i = random.randint(1, 363)
        country_id = Country.objects.create(title=country,
                                            content=fake.text(),
                                            img='images/country/' + str(i) + '.jpg'
                                            ).id
        for j in range(20):
            country = fake.country()
            while Country.objects.filter(title=country).exists():
                country = fake.country()
            i = random.randint(1, 363)

            country = Country.objects.create(title=country,
                                             content=fake.text(),
                                             img='images/country/' + str(i) + '.jpg'
                                             )
        # creating cities
        city = fake.city()
        i = random.randint(1, 363)
        city_id = City.objects.create(title=city,
                                      content=fake.text(),
                                      img='images/country/' + str(i) + '.jpg',
                                      country=Country.objects.get(id=random.randint(country_id, country_id + 19))
                                      ).id
        for j in range(100):
            city = fake.city()
            while City.objects.filter(title=city).exists():
                city = fake.city()
            i = random.randint(1, 363)
            City.objects.create(title=city,
                                content=fake.text(),
                                img='images/country/' + str(i) + '.jpg',
                                country=Country.objects.get(id=random.randint(country_id, country_id + 19))
                                )
        # creating regions
        regions = ["Европа", "Азия", "Океания", "Америка", "Африка", "Австаралия"]
        i = random.randint(1, 399)

        region_id = Region.objects.create(title='Холодные зоны',
                                          background_img='images/region/' + str(
                                              i) + '.jpg',
                                          logo_outline='images/region/' + str(
                                              i) + '.jpg').id
        for j in range(6):
            region = regions[j]
            i = random.randint(1, 399)
            Region.objects.create(title=region,
                                  background_img='images/region/' + str(i) + '.jpg',
                                  logo_outline='images/region/' + str(i) + '.jpg')
        Faker.seed(0)
        # creating users
        id = 0
        for j in range(50):
            username = fake.simple_profile()['username']
            email = fake.email()
            password = fake.password()
            fake_data = {
                'register_url': "/auth/users/",
                'activate_url': "/auth/users/activation/",
                'login_url': "/auth/jwt/create",
                'user_details_url': "/auth/users/me/",
                'user_data': {
                    "email": email,
                    "username": username,
                    "password": password,
                    "region": Region.objects.get(id=random.randint(region_id, region_id + 5)).slug,
                    "city": City.objects.get(id=random.randint(city_id, city_id + 100)).slug,
                },
                'login_data': {
                    "email": email,
                    "password": password
                }, }
            id = Snippet.create_full_user(self, fake_data)
        Faker.seed(0)
        i = random.randint(1, 399)
        tags_names= ["Пляж","Горы","Пустыни","Комфорт","Холод","Жара","Дорого","Дёшево","Экзотично","Острова","Опасно","Безопасно"]
        tag_id = Tag.objects.create(name="Казино").id
        for j in tags_names:
            Tag.objects.create(name=j)
        text = fake.text();
        for j in range(10):
            text+=fake.text()
        for ii in range(100):
            for j in range(10):
                text += fake.text()
            i = random.randint(1, 363)
            post = Article.objects.create(title=fake.text()[:100],
                                   description=fake.text()[:200],
                                   content=text,
                                   author_id=random.randint(id-49, id),
                                    img ='images/region/' + str(i) + '.jpg'
                                   )
            count = random.randint(0, 10)
            for k in range(count):
                post.city.add(City.objects.get(id=random.randint(city_id, city_id + 100)));
            count = random.randint(0, 10)
            for k in range(count):
                post.country.add(Country.objects.get(id=random.randint(country_id, country_id + 20)));
            count = random.randint(0, 10)
            for k in range(count):
                post.tags.add(Tag.objects.get(id=random.randint(tag_id, tag_id + 10)));


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserTest(APITestCase):
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

        self.region = Region.objects.create(title='region')
        for i in range(15):
            Region.objects.create(title='region' + str(i))

    def test_register_with_email_verification(self):
        Snippet.register_with_email_verification(self, self.data)

    def test_list_regions(self):
        response = self.client.get(reverse('regions'))
        serializer = RegionSerializer(Region.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_region(self):
        response = self.client.get(reverse('region', kwargs={'slug': self.region.slug}), format='json')
        serializer = RegionSerializer(Region.objects.get(slug=self.region.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_user(self):
        self.user = Userc.objects.get(email=Snippet.register_with_email_verification(self, self.data).get('email'))
        response = self.client.get(reverse('profile', kwargs={'slug': self.user.slug}), format='json')
        serializer = UserProfileSerializer(Userc.objects.get(slug=self.user.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), serializer.data.get('email'))

    def test_login_user_valid(self):
        Snippet.register_with_email_verification(self, self.data)
        response = self.client.post(self.data.get('login_url'), self.data.get('login_data'), format="json")
        self.assertTrue("access" in response.json())
        token = response.json()["access"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # get user details
        response = self.client.get(self.data.get('user_details_url'), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.data.get('user_data')["email"])
        self.assertEqual(response.data["username"], self.data.get('user_data')["username"])

    def test_login_user_invalid(self):
        Snippet.register_with_email_verification(self, self.data)

        response = self.client.post(self.data.get('login_url'), self.data.get('login_data'), format="json")
        self.assertTrue("access" in response.json())
        token = "odosjfpoo"
        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # get user details
        response = self.client.get(self.data.get('user_details_url'), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_popular_authors(self):
        for i in range(15):
            data = {
                'register_url': "/auth/users/",
                'activate_url': "/auth/users/activation/",
                'login_url': "/auth/jwt/create",
                'user_details_url': "/auth/users/me/",
                'user_data': {
                    "email": "test@example.com" + str(i),
                    "username": "test_user" + str(i),
                    "password": "verysecret" + str(i),
                },
                'login_data': {
                    "email": "test@example.com" + str(i),
                    "password": "verysecret" + str(i)
                }, }
            user = Userc.objects.get(slug=Snippet.register_with_email_verification(self, data).get('slug'))

            post = Article.objects.create(title='1 post' + str(i),
                                          description='1post lorem1post lorem1post lorem' + str(i),
                                          content='1post lorem 1post lorem1post lorem1post lorem1post lorem1post lorem',
                                          author=user,
                                          )
            post.views = i
            post.save()
            user.save()

        response = self.client.get(reverse('popular_authors'))
        data_serialized = UserProfileSerializer(Userc.objects.all().order_by('-points')[:4], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("points"), data_serialized.data[0].get("points"))

    def test_following_valid(self):
        Snippet.follow_unfollow(self)

    def test_unfollowing_valid(self):
        user1, user2 = Snippet.follow_unfollow(self)
        response = self.client.post(reverse('unfollow', kwargs={'pk': user1.id}), {'id': user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get("followers")), 0)

    def test_edit_profile(self):
        data = {
            "region": self.region.slug,
            "bio": "testbiotext",
            "email": "test@example.com",
        }
        user = Userc.objects.get(slug=Snippet.register_with_email_verification(self, self.data).get('slug'))
        response = self.client.put(reverse('profile_edit', kwargs={'slug': user.slug}), data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('region'), data.get('region'))

    def test_acreation_users(self):
        Snippet.auto_user(self)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()



