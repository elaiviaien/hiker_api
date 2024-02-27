from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ContactsTests(APITestCase):
    def test_send_mail(self):
        data = {
            'subject': 'test',
            'email': 'test',
            'message': 'test',
            'name': 'test'
        }
        response = self.client.post(reverse('send_mail'),data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
