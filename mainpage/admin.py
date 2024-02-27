from django.contrib import admin

from .models import Article, Picture, Tag
from city_country.models import Country, City
from comment.models import Comment
from users.models import Userc, Region, TicketOrder

admin.site.register(Userc)
admin.site.register(Comment)


class PostImageAdmin(admin.StackedInline):
    """additional method for multiple images"""
    model = Picture


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    """regists article in admin panel"""


@admin.register(TicketOrder)
class TicketOrder(admin.ModelAdmin):
    """regists article in admin panel"""

    class Meta:
        model = TicketOrder


@admin.register(Picture)
class PostImageAdmin(admin.ModelAdmin):
    """regists pictures in admin panel"""

    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """regists tags in admin panel"""

    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """regists countries in admin panel"""

    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """regists cities in admin panel"""

    pass

@admin.register(Region)
class Region(admin.ModelAdmin):
    """regists region in admin panel"""

    pass
