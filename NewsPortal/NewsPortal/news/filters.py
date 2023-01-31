from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='post_add_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'post_header': ['icontains'],
            'post_category': ['exact'],
        }
