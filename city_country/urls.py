from django.urls import path

from .views import ProfileCity, ProfileCountry, Country, City

urlpatterns = [

    path('country/<slug:slug>', ProfileCountry.as_view(), name='country_profile'),
    path('city/<slug:slug>', ProfileCity.as_view(), name='city_profile'),
    path('country', Country.as_view(), name='country'),
    path('city', City.as_view(), name='city'),


]

