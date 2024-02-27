import requests
from django.shortcuts import redirect
from django.views import View
from msrest.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, get_object_or_404, ListAPIView, CreateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import Userc, Region, TicketOrder
from .serializers import UserProfileSerializer, UserUpdateSerializer, RegionSerializer, TicketSerializer, \
    CreateTicketSerializer


class follow(APIView):
    """view for follows"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Userc.objects.all(), id=pk)
        post.followers.add(request.POST.get('id'))
        serializer = UserProfileSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class unfollow(APIView):
    """view for unfollows"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Userc.objects.all(), id=pk)
        post.followers.remove(request.POST['id'])
        serializer = UserProfileSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Profile(RetrieveAPIView):
    """view of user`s profile"""
    serializer_class = UserProfileSerializer
    queryset = Userc.objects.all()
    lookup_field = 'slug'


class Ticket(RetrieveAPIView):
    """view of user`s profile"""
    serializer_class = TicketSerializer
    queryset = TicketOrder.objects.all()
    lookup_field = 'slug'


class ProfileUpdate(UpdateAPIView):
    """view for updating profile"""
    serializer_class = UserUpdateSerializer
    queryset = Userc.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        username = self.request.user.id
        if int(username) != int(self.get_object().id):
            return Response({'success': False, 'message': "Can't delete this"}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PopularAuthors(ListAPIView):
    """view of list of posts"""
    serializer_class = UserProfileSerializer
    pagination_class = None

    def get_queryset(self):
        return Userc.objects.all().filter(is_active=True).order_by('-points')[:4]


class CreateTicket(CreateAPIView):
    serializer_class = CreateTicketSerializer
    permission_classes = [IsAuthenticated]


class DeleteTicket(DestroyAPIView):
    """view for deleting article"""
    serializer_class = TicketSerializer
    queryset = TicketOrder.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class ListTicket(ListAPIView):
    """view of list of posts"""
    serializer_class = TicketSerializer
    queryset = TicketOrder.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.kwargs['slug']
        return TicketOrder.objects.all().filter(user__slug=user).order_by('-date')


class Regions(ListAPIView):
    """view of list of posts"""
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    pagination_class = None


class Region(RetrieveAPIView):
    """view of list of posts"""
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    lookup_field = 'slug'


class UserActivationView(View):

    def get(self, request, uid, token, format=None):
        response = redirect('https://hiker-travel.herokuapp.com/users/activation/' + uid + '/' + token)
        return response


class ResetPasswordView(View):
    def get(self, request, uid, token, format=None):
        response = redirect('https://hiker-travel.herokuapp.com/users/reset_password/' + uid + '/' + token)
        return response
