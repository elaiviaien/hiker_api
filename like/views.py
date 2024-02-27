from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mainpage.models import Article
from mainpage.serializers import PostCreateSerializer
from users.models import Userc


class like(APIView):
    """view for likes"""
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(Article.objects.all(), id=pk)
        post.likes.add(request.POST['id'])
        user = Userc.objects.get(slug = post.author.slug)
        #user.points = user.points+7
        post.points = post.points+7
        post.save()
        user.save()
        print(user.points)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class unlike(APIView):
    """view for unlikes"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Article.objects.all(), id=pk)
        post.likes.remove(request.POST['id'])
        #user.points = user.points-7
        #post.points = post.points-7
        post.save()
        user = Userc.objects.get(slug = post.author.slug)
        user.save()
        print(user.points)

        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
