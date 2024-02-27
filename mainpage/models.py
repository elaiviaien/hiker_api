from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from slugify import slugify
from city_country.models import City, Country
from users.models import Userc

from io import BytesIO

from PIL import Image
from django.core.files import File


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im = im.convert('RGB')
    im.save(im_io, 'JPEG', quality=70)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


class Tag(models.Model):
    """model for tags """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.name))

        # save
        super().save(*args, **kwargs)


class Article(models.Model):
    """model for posts"""
    author = models.ForeignKey(Userc, related_name='post_author', on_delete=models.CASCADE, verbose_name='Автор',
                               default=None, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default=None)
    content = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True, editable=False)

    likes = models.ManyToManyField(Userc, default=None, blank=True)
    img = models.ImageField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='post_tags', verbose_name='Теги', blank=True)
    city = models.ManyToManyField(City, related_name='post_cities', blank=True)
    country = models.ManyToManyField(Country, related_name='post_countries', blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    views = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #if self.views != 0:
        #    self.points = self.views + self.likes.all().count() * 7 + self.comments.filter(
        #        approved_comment=True).count() * 25

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('poster', kwargs={'slug': self.slug})

    def get_absolute_url_edit(self):
        return reverse('edit', kwargs={'slug': self.slug})

    def get_absolute_url_del(self):
        return reverse('delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.title))
        if self.views != 0:
            self.points = self.views + self.likes.all().count() * 7 + self.comments.filter(
                approved_comment=True).count() * 25
        # save
        super().save(*args, **kwargs)


class Location(models.Model):
    lng = models.DecimalField(max_digits=15, decimal_places=12)
    lat = models.DecimalField(max_digits=15, decimal_places=12)
    post = models.ForeignKey(Article, default=0, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='waypoints')


class Picture(models.Model):
    """model for pictures"""
    post = models.ForeignKey(Article, default=None, on_delete=models.CASCADE, null=True, blank=True)
    url = models.ImageField(blank=True, null=True)
    upload = models.ImageField(blank=True, null=True)

    def __str__(self):
        if self.post:
            return self.post.title
        else:
            return str(self.url)

    def save(self, *args, **kwargs):
        # call the compress function
        if(self.url):
            new_image = compress(self.url)
        else:
            new_image = compress(self.upload)
        # # set self.image to new_image
        self.url = new_image
        self.upload = new_image
        # save
        self.upload =self.url
        super().save(*args, **kwargs)
