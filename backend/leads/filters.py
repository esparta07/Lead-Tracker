# filters.py
import django_filters
from core.models import Lead

class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = {
            'date': ['exact', 'gte', 'lte'],
            'company_name': ['exact', 'icontains'],
            'assigned__id': ['exact'],
            'source__id': ['exact'],
            'sub_source__id': ['exact'],
            'lead_status__id': ['exact'],
        }
