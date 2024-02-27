from django.urls import path

from .views import CommentCreate,  CommentDelete


urlpatterns = [

    path('comment_create/<slug:slug>', CommentCreate.as_view(), name='create_comment'),
    path('comment_delete/<int:pk>', CommentDelete.as_view(), name='delete_comment'),



]

