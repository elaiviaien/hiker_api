from rest_framework import serializers


from city_country.models import Country, City
from comment.models import Comment
from comment.serializers import ReviewSerializer
from users.models import  Region
from .models import Article, Tag, Picture, Location


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields= '__all__'




class TagSerializer(serializers.ModelSerializer):
    """serializer for tags"""

    class Meta:
        model = Tag
        fields = ("name", "id","slug")



class LocationSerializer(serializers.ModelSerializer):
    lng = serializers.DecimalField(max_digits=15, decimal_places=12, required=False)
    lat = serializers.DecimalField(max_digits=15, decimal_places=12, required=False)
    post = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
class PostListSerializer(serializers.ModelSerializer):
    """serializer for list of posts"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = serializers.SerializerMethodField('get_comments')
    likes = serializers.SlugRelatedField(slug_field="username", read_only=True, many=True)
    views = serializers.IntegerField()
    points = serializers.IntegerField()
    date = serializers.DateTimeField()
    waypoints = LocationSerializer(many=True)
    class Meta:
        model = Article
        fields = ("title", "date", "author", "id", "slug", "comments", "img", "tags", "likes", "views", "points","description","city","country","waypoints")
    def get_comments(self, post):
        qs = Comment.objects.filter(approved_comment=True, post=post)
        serializer = ReviewSerializer(instance=qs, many=True)
        return serializer.data



class PostSerializer(serializers.ModelSerializer):
    """serializer for single post"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    likes = serializers.SlugRelatedField(slug_field="username", read_only=True, many=True)
    comments = serializers.SerializerMethodField('get_comments')
    views = serializers.IntegerField(required=False)
    date = serializers.DateTimeField(required=False)
    city = serializers.SlugRelatedField(queryset=City.objects.all(), many=True, slug_field="title")
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), many=True, slug_field="title")
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field="name")
    img = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    waypoints = LocationSerializer(many=True)

    def get_comments(self, post):
        qs = Comment.objects.filter(approved_comment=True, post=post)
        serializer = ReviewSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Article
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    """serializer for creating post"""

    author_id = serializers.IntegerField(write_only=True)
    city = serializers.SlugRelatedField(queryset=City.objects.all(), many=True, slug_field="slug")
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), many=True, slug_field="slug")
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field="slug")


    img = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Article
        fields = "__all__"


class UploadImg(serializers.ModelSerializer):
    """serializer for uploading img"""

    post = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Picture
        fields = ("post", "url", "upload")


