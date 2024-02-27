
from rest_framework.generics import RetrieveAPIView, ListAPIView


from .models import Country, City
from .serializers import CountryProfileSerializer, CityProfileSerializer


class ProfileCountry(RetrieveAPIView):
    """view of country`s profile"""
    serializer_class = CountryProfileSerializer
    queryset = Country.objects.all()
    lookup_field = "slug"


class ProfileCity(RetrieveAPIView):
    """view of city`s profile"""
    serializer_class = CityProfileSerializer
    queryset = City.objects.all()
    lookup_field = "slug"


class Country(ListAPIView):
    """view of country`s profile"""
    serializer_class = CountryProfileSerializer
    queryset = Country.objects.all()
    pagination_class = None

class City(ListAPIView):
    """view of city`s profile"""
    serializer_class = CityProfileSerializer
    queryset = City.objects.all()
    pagination_class = None
