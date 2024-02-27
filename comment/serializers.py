from rest_framework import serializers


from .models import Comment
from users.serializers import UserProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """serializer for comments"""

    post = serializers.SlugRelatedField(slug_field='title', read_only=True)
    author = UserProfileSerializer()
    created_date = serializers.DateTimeField()

    class Meta:
        model = Comment
        fields = ("author", "text", "created_date", "post", "id")



class ReviewCreateSerializer(serializers.ModelSerializer):
    """serializer for comments creating"""

    post = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


