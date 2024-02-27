
from django.contrib import admin
from django.urls import path, include, re_path

from users.views import UserActivationView, ResetPasswordView
from . import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [

    path('api/v1/', include('mainpage.urls')),
    path('api/v1/', include('city_country.urls')),
    path('api/v1/', include('comment.urls')),
    path('api/v1/', include('contacts.urls')),
    path('api/v1/', include('like.urls')),
    path('api/v1/', include('users.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view()),
    path('password/reset/confirm/<str:uid>/<str:token>', ResetPasswordView.as_view()),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
