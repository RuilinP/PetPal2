import django_filters
from .models import Pet

class PetFilter(django_filters.FilterSet):
    class Meta:
        model = Pet
        fields = {
            'status': ['exact'],
            'specie': ['exact'],
            'breed': ['exact'],
            'age': ['exact', 'lt', 'gt'],
            'size': ['exact'],
            'color': ['exact'],
            'gender': ['exact'],
            'shelter': ['exact'],
        }
