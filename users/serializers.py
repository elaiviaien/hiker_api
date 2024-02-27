from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from city_country.models import City
from mainpage.models import Picture
from users.models import Userc, Region, TicketOrder


def get_file_extension(file_name, decoded_file):
    import imghdr

    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension

    return extension


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CreateTicketSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TicketOrder
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    date = serializers.DateTimeField(required=False)

    class Meta:
        model = TicketOrder
        fields = ('user', 'text_id','id','date','slug')


class UserProfileSerializer(serializers.ModelSerializer):
    """serializer for user's profile"""

    points = serializers.IntegerField()
    city = CitySerializer()
    region = RegionSerializer()

    class Meta:
        model = Userc
        exclude = ('password',)


class UploadImg(serializers.ModelSerializer):
    """serializer for uploading img"""

    post = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Picture
        fields = ("post", "url", "upload")


class UserCreateSerializer(UserCreateSerializer):
    """serializer for creating user*for simple jwt*"""

    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field="slug", required=False)
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field="slug", required=False)

    class Meta(UserCreateSerializer.Meta):
        model = Userc
        fields = ("id", "username", "password", "email", "bio", "city", "region")


class UserUpdateSerializer(serializers.ModelSerializer):
    """serializer for updating user"""

    profile_img = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field="slug", required=False)
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field="slug", required=False)

    class Meta:
        model = Userc
        fields = ("email", "profile_img", "id", "first_name", "bio", "city", "region")
