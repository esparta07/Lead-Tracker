# urls.py
from django.urls import path
from .views import (
    FileUploadView,
    LeadListCreateAPIView,
    LeadRetrieveUpdateDestroyAPIView,
    SourceListCreateAPIView,
    SourceRetrieveUpdateDestroyAPIView,
    SubSourceListCreateAPIView,
    SubSourceRetrieveUpdateDestroyAPIView,
    StatusListCreateAPIView,
    StatusRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('leads/', LeadListCreateAPIView.as_view(), name='lead-list-create'),
    path('leads/<int:pk>/', LeadRetrieveUpdateDestroyAPIView.as_view(), name='lead-detail'),
    path('sources/', SourceListCreateAPIView.as_view(), name='source-list'),
    path('sources/<int:pk>/', SourceRetrieveUpdateDestroyAPIView.as_view(), name='source-detail'),
    path('sub-sources/', SubSourceListCreateAPIView.as_view(), name='sub-source-list'),
    path('sub-sources/<int:pk>/', SubSourceRetrieveUpdateDestroyAPIView.as_view(), name='sub-source-detail'),
    path('statuses/', StatusListCreateAPIView.as_view(), name='status-list'),
    path('statuses/<int:pk>/', StatusRetrieveUpdateDestroyAPIView.as_view(), name='status-detail'),
]
