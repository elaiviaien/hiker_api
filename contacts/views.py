from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.serializers import SendMail
from hiker.settings import EMAIL_HOST_USER


class SendEmail(APIView):
    def post(self, request):
        serializer = SendMail(request.data)
        subject = serializer.data['subject']
        message = serializer.data['message']
        recepient = str(serializer.data['email'])
        message+='\nsender: '+recepient
        name= serializer.data['name']
        message+='\nname: '+name
        send_mail(subject,
                  message, EMAIL_HOST_USER,[EMAIL_HOST_USER],  fail_silently=False)
        return Response(serializer.data)

