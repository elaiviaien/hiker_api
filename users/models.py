import shutil

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from slugify import slugify
from django.utils.translation import ugettext_lazy as _

from io import BytesIO

from PIL import Image
from django.core.files import File
from city_country.models import City
from hiker import settings


class UserManager(BaseUserManager):

    def create_user(self,*args, **kwargs):
        if kwargs.get('email') is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(kwargs.get('email')), username=kwargs.get('username'),
                          city=kwargs.get('city'), region=kwargs.get('region'), bio=kwargs.get('bio'))
        user.set_password(kwargs.get('password'))
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email = email, password=password,username = email)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
def compress(image):
    with Image.open(image) as im:
        # create a BytesIO object
        im_io = BytesIO()
        # save image to BytesIO object
        im = im.convert('RGB')

        im.save(im_io, 'JPEG', quality=70)
        # create a django-friendly Files object
        new_image = File(im_io, name=image.name)
        image.close()
    return new_image




class Region(models.Model):
    """model for cities"""
    title = models.CharField(max_length=255)
    background_img = models.ImageField(null=True)
    logo_outline = models.ImageField(null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """slugifies title"""
        self.slug = (slugify(self.title))
        super(Region, self).save(*args, **kwargs)


class Userc(AbstractUser):
    """model for users"""

    profile_img = models.ImageField(null=True,blank=True)
    bio = RichTextUploadingField(null=True, blank=True)
    city = models.ForeignKey(City, related_name='bb', on_delete=models.CASCADE, default=None, null=True, blank=True)
    followers = models.ManyToManyField('Userc', blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    points = models.IntegerField(default=0)
    region = models.ForeignKey(Region, related_name='user_region', on_delete=models.SET_NULL, verbose_name='регион',
                               default=None, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #posts_points = self.post_author.all()
        #p = 0
        #for post in posts_points:
        #    p += post.points

        #self.points = p


    def save(self, *args, **kwargs):
        """counts points of user"""
        posts_points = self.post_author.all()
        p = 0
        for post in posts_points:
            p += post.points
        self.points = p
        self.slug = (slugify(self.username))

        #if not self.profile_img:
        #    shutil.copyfile('test.jpg', settings.MEDIA_ROOT + r"\test.jpg")
        #    i = File(open(settings.MEDIA_ROOT + r'\test.jpg', 'rb'))
        #    new_image = compress(i)
        #else:
         #   new_image = compress(self.profile_img)
        #    set self.image to new_imagex
       # self.profile_img = new_image


        super(Userc, self).save(*args, **kwargs)


class TicketOrder(models.Model):
    """model for tickets"""

    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    text_id = models.CharField(max_length=100,unique=True, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    user = models.ForeignKey(Userc,related_name='user_tickets',on_delete=models.CASCADE, verbose_name="Пользователь",    default=None, blank=True, null=True)

    def __str__(self):
        return self.slug


    def save(self, *args, **kwargs):
        """slugifies title"""
        self.slug = (slugify(self.text_id))
        super(TicketOrder, self).save(*args, **kwargs)