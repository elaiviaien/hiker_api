from django.urls import path

from mainpage.views import UploadImage
from .views import Profile, ProfileUpdate, follow, unfollow, PopularAuthors, Regions, Region, Ticket, CreateTicket, \
    DeleteTicket, ListTicket

urlpatterns = [
    path('popular_authors', PopularAuthors.as_view(), name='popular_authors'),
    path('follow/<int:pk>', follow.as_view(), name='follow'),
    path('unfollow/<int:pk>', unfollow.as_view(), name='unfollow'),
    path('regions', Regions.as_view(), name='regions'),
    path('regions/<slug:slug>', Region.as_view(), name='region'),
    path('<slug:slug>/', Profile.as_view(), name='profile'),
    path('ticket/<slug:slug>', Ticket.as_view(), name='ticket'),
    path('create_ticket', CreateTicket.as_view(), name='create_ticket'),
    path('list_tickets/<slug:slug>', ListTicket.as_view(), name='list_ticket'),
    path('delete_ticket/<slug:slug>', DeleteTicket.as_view(), name='delete_ticket'),
    path('profile_edit/<slug:slug>/', ProfileUpdate.as_view(), name='profile_edit'),
    path('upload_img/<slug:slug>/', UploadImage.as_view(), name='upload_image'),
]

