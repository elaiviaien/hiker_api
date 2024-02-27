import shutil
import tempfile

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from city_country.models import City, Country
from city_country.serializers import CityProfileSerializer, CountryProfileSerializer
from hiker import settings


MEDIA_ROOT = tempfile.mkdtemp()
shutil.copyfile('/graphics/test.jpg', MEDIA_ROOT + r"\test.jpg")


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class CityCountryTests(APITestCase):

    def setUp(self):
        settings.MEDIA_ROOT = MEDIA_ROOT
        self.country = Country.objects.create(title='test',
                                              content='test',
                                              img="hiker/media/test.jpg"
                                              )
        for i in range(15):
            Country.objects.create(title='test' + str(i),
                                   content='test' + str(i),
                                   img="hiker/media/test.jpg"
                                   )
        self.city = City.objects.create(title='testc',
                                        content='testc',
                                        img="hiker/media/test.jpg",
        country=Country.objects.get(slug=('test'))
                                        )
        for i in range(15):
            City.objects.create(title='testc' + str(i),
                                content='testc' + str(i),
                                img="hiker/media/test.jpg",
                                country=Country.objects.get(slug=('test' + str(i)))
                                )

    def test_list_cities(self):
        response = self.client.get(reverse('city'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(City.objects.all()))

    def test_list_countries(self):
        response = self.client.get(reverse('country'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Country.objects.all()))

    def test_detail_city(self):
        response = self.client.get(reverse('city_profile', kwargs={'slug':self.city.slug}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.city.title)

    def test_detail_country(self):
        response = self.client.get(reverse('country_profile', kwargs={'slug': self.country.slug}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.country.title)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()