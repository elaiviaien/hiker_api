from django.urls import path

from .views import SendEmail


urlpatterns = [

    path('send_mail', SendEmail.as_view(), name='send_mail'),


]

