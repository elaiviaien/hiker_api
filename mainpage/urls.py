from django.urls import path

from .views import ArticleCreate, ArticleDelete, ArticleUpdate, BlogList, BlogDetail, ArticleCreatePosts, TagList, \
    AddView, AddPoint, SetPoints

urlpatterns = [

    path('create', ArticleCreate.as_view(), name='create'),
    path('cabinet/<slug:slug>', ArticleCreatePosts.as_view(), name='create_cab'),
    path('delete/<slug:slug>', ArticleDelete.as_view(), name='delete'),
    path('edit/<slug:slug>', ArticleUpdate.as_view(), name='edit'),
    path('add_view/<slug:slug>', AddView.as_view(), name='add_view'),
    path('blog', BlogList.as_view(), name='blog'),
    path('tags', TagList.as_view(), name='tags'),
    path('blog/<slug:slug>', BlogDetail.as_view(), name='post'),
    path('add_point/<slug:slug>', AddPoint.as_view(), name='add_point'),
    path('set_points/<slug:slug>', SetPoints.as_view(), name='set_points'),




]

