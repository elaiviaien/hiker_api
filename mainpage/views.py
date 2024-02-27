from django.core.files import File
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from comment.views import secure
from users.models import Userc
from .models import Article, Tag, compress, Location
from .serializers import PostListSerializer, PostSerializer, PostCreateSerializer, TagSerializer, UploadImg, \
    LocationSerializer
from .services import FilteredListView


class ArticleCreate(CreateAPIView):
    """view for creating article"""
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data.get('img'):
            new_image = compress(serializer.validated_data.get('img'))
            serializer.save(img=new_image)
        else:
            serializer.save()


class ArticleCreatePosts(ListAPIView):
    """view of list of posts"""

    queryset = Article.objects.filter()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author = self.kwargs['slug']
        return Article.objects.all().filter(author__slug=author).order_by('-date')


class ArticleDelete(DestroyAPIView):
    """view for deleting article"""
    serializer_class = PostSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):

        username = self.request.user.email
        if str(self.get_object().author) != str(username):
            return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(self.get_object())
        return Response({'success': True, 'message': "Deleted"}, status=status.HTTP_204_NO_CONTENT)


class ArticleUpdate(UpdateAPIView):
    """view for updating of article"""
    serializer_class = PostCreateSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        username = self.request.user.id
        if username != self.get_object().author_id:
            return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if serializer.validated_data.get('img'):
            new_image = compress(serializer.validated_data.get('img'))
            serializer.save(img=new_image)
        else:
            serializer.save()


class BlogList(ListAPIView):
    """view of list of posts"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilteredListView

    def get_queryset(self):
        return Article.objects.filter(title__icontains=self.request.GET.get("search")).order_by('-id')

    serializer_class = PostListSerializer


class BlogDetail(RetrieveAPIView):
    """view of blog`s detail"""
    queryset = Article.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"


class UploadImage(CreateAPIView):
    """view for uploading image"""

    serializer_class = UploadImg

    def perform_create(self, serializer):

        if self.kwargs.get('slug') != "none":

            serializer.save(post=Article.objects.get(slug=self.kwargs.get('slug')))

        else:
        #     if serializer.validated_data['upload']:
        #         print(serializer.validated_data['upload'])
        #
        #         serializer.save(url="https://hiker-bucket-assets.s3.amazonaws.com/dcb00a3a-eee.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQ3KTD3JPX7PUVGVV%2F20220713%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220713T154058Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a99917a5bcb074fe9f27e96dfb732246e896bec7d8919e020131658bfb3c4146")
        #     else:
            serializer.save()


class AddView(APIView):
    """view of addaing view for post"""

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        article.views = article.views + 1
        article.save()
        user = Userc.objects.get(slug = article.author.slug)
        user.save()
        serializer = PostSerializer(article)
        return Response(serializer.data)


class TagList(ListAPIView):
    """view of list of posts"""

    def get_queryset(self):
        return Tag.objects.all()

    pagination_class = None
    serializer_class = TagSerializer


class AddPoint(CreateAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        username = self.request.user.id
        author = Article.objects.get(slug = kwargs['slug']).author_id
        if str(username) != str(author):
            return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(post=Article.objects.get(slug=self.kwargs.get('slug')))


class SetPoints(APIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):

        username = self.request.user.id
        author = Article.objects.get(slug = slug).author_id
        if str(username) != str(author):
            return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)
        points = Location.objects.all().filter(post__slug=slug)
        points.delete()
        return Response("deleted all points")
