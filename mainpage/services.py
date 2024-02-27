from django_filters import rest_framework as filters, ModelMultipleChoiceFilter, ChoiceFilter

from city_country.models import City, Country
from mainpage.models import Article, Tag


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class FilteredListView(filters.FilterSet):
    """filter for BlogListView"""
    tags = ModelMultipleChoiceFilter(field_name='tags__slug', to_field_name="slug",
                                     queryset=Tag.objects.all())
    city = ModelMultipleChoiceFilter(field_name='city__slug', to_field_name="slug",
                                     queryset=City.objects.all())
    country = ModelMultipleChoiceFilter(field_name='country__slug', to_field_name="slug",
                                        queryset=Country.objects.all())
    CHOICES = (
        ('ascending', 'По ворастанию'),
        ('descending', 'По убыванию')
    )
    ordering = ChoiceFilter(label='Порядок', choices=CHOICES, method='filter_by_order')

    date = filters.DateRangeFilter()

    def filter_by_order(self, queryset, name, value):
        """function for django filter by points"""
        expression = 'points' if value == 'ascending' else '-points'
        return queryset.order_by(expression)

    class Meta:
        model = Article
        fields = ['tags', 'date', 'city', 'country']