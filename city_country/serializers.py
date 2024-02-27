from rest_framework import serializers


from .models import Country, City



class CountryProfileSerializer(serializers.ModelSerializer):
    """serializer for country's profile"""

    class Meta:
        model = Country
        fields = ("title", "content", "slug", "img", "id")


class CityProfileSerializer(serializers.ModelSerializer):
    """serializer for city's profile"""

    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field="slug")

    class Meta:
        model = City
        fields = ("title", "content", "slug", "img", "country", "id")



