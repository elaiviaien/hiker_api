from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from mainpage.models import Article
from mainpage.serializers import ReviewSerializer
from users.models import Userc

from .models import Comment
from .serializers import ReviewCreateSerializer


def secure(self, request, *args, **kwargs):

    username = self.request.user.id
    if username != self.get_object().author_id:
        return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)


class CommentCreate(CreateAPIView):
    """view for creating comment"""
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs.get('slug'))

        serializer.save(post=article)


class CommentDelete(DestroyAPIView):
    """view for creating comment"""
    serializer_class = ReviewSerializer
    queryset = Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        secure(self, request, *args, **kwargs)
        self.perform_destroy(self.get_object())
        return Response({'success': True, 'message': "Deleted"}, status=status.HTTP_204_NO_CONTENT)
