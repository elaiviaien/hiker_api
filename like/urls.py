from django.urls import path

from .views import like, unlike


urlpatterns = [

    path('like/<int:pk>', like.as_view(), name='like'),
    path('unlike/<int:pk>', unlike.as_view(), name='unlike'),



]

