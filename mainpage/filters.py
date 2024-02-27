import django_filters
from .models import Article


def filter_by_order(queryset, value):
    """function for django filter by date"""
    expression = 'points' if value == 'ascending' else '-points'
    return queryset.order_by(expression)


class ArticlesFilter(django_filters.FilterSet):
    """class for django filter of articles"""
    CHOICES = (
        ('ascending', 'По ворастанию'),
        ('descending', 'По убыванию')
    )
    ordering = django_filters.ChoiceFilter(label='Порядок', choices=CHOICES, method='filter_by_order')
    class Meta:
        model = Article
        fields = ['tags', 'city']
