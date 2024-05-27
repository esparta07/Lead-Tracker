import csv
from io import StringIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .serializers import FileUploadSerializer,LeadSerializer,SourceSerializer, SubSourceSerializer, StatusSerializer
from core.models import Lead, User, Source, SubSource,Source, SubSource, Status, Campaign
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from core.models import Lead
from .serializers import LeadSerializer
from .filters import LeadFilter
from django.core.exceptions import ValidationError
import os
from django.utils import timezone
from rest_framework import generics

from core.permissions import ReadOnlyOrAdminPermission
from rest_framework import permissions


class SourceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class SourceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class SubSourceListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubSource.objects.all()
    serializer_class = SubSourceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class SubSourceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubSource.objects.all()
    serializer_class = SubSourceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

class LeadListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = LeadFilter
    search_fields = ['company_name', 'point_of_contact', 'email']
    ordering_fields = ['date', 'company_name']

class LeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=FileUploadSerializer,
        responses={201: {'description': 'File processed and leads added'}, 400: {'description': 'Bad request'}}
    )
    def post(self, request, *args, **kwargs):
        """
        Uploads a file and processes it based on the processing_type.

        ---
        parameters:
          - name: file
            required: true
            type: file
            description: The file to upload
          - name: processing_type
            required: true
            type: string
            description: The processing type (0 or 1)
            enum: ["0", "1"]
        responses:
          201:
            description: File processed and leads added
          400:
            description: Bad request
        """
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            processing_type = serializer.validated_data.get('processing_type', '0')

            # Check file type
            if not self.is_valid_file_type(file):
                return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

            if processing_type == '0':
                
                # Process the file according to the predefined format
                data_set = file.read().decode('UTF-8')
                io_string = StringIO(data_set)
                csv_reader = csv.reader(io_string, delimiter=',')

                # Skip the header row
                next(csv_reader)
                
                
                # Process each row
                for row in csv_reader:
                    date, company_name, point_of_contact, phone_number, email, source_name, sub_source_name = row

                    # Fetch or create related objects
                    source, _ = Source.objects.get_or_create(name=source_name)
                    sub_source, _ = SubSource.objects.get_or_create(name=sub_source_name, source=source)

                    # Create the Lead object with status=None
                    Lead.objects.create(
                        date=date,
                        company_name=company_name,
                        point_of_contact=point_of_contact,
                        phone_number=phone_number,
                        email=email,
                        source=source,
                        sub_source=sub_source,
                        lead_status=None
                    )

                return Response({'status': 'file processed'}, status=status.HTTP_201_CREATED)
            
            elif processing_type == '1':
                # Process the file according to the Facebook CSV format
                data_set = file.read().decode('UTF-8')
                io_string = StringIO(data_set)
                csv_reader = csv.reader(io_string, delimiter=',')

                # Skip the header row
                next(csv_reader)

                # Process each row
                for row in csv_reader:
                    Created, Name, Email, Source, Form, Channel, Stage, Owner, Labels, Phone = row

                    # Parse the date
                    date = timezone.datetime.strptime(Created, "%m/%d/%y, %I:%M%p")

                    # Fetch or create related objects
                    # source, _ = Source.objects.get_or_create(name=Source)
                    campaign, _ = Campaign.objects.get_or_create(campaign_name=Form,campaign_source='Facebook')
                    
                    # Assuming sub_source is somehow derived from the CSV, handle accordingly

                    # Create the Lead object with status=None
                    Lead.objects.create(
                        date=date,
                        company_name=None,
                        point_of_contact=Name,  # If point_of_contact is available in CSV, replace None with the correct value
                        phone_number=Phone,
                        email=Email,
                        source=None,
                        sub_source=None,  # If sub_source can be derived, handle it accordingly
                        lead_status=None  # If lead_status can be derived from Stage or other fields, handle it accordingly
                    )

                return Response({'status': 'file processed'}, status=status.HTTP_201_CREATED)

            
            elif processing_type == '2':
                # Process the file according to the website format
                data_set = file.read().decode('UTF-8')
                io_string = StringIO(data_set)
                csv_reader = csv.reader(io_string, delimiter=',')

                # Skip the header row
                next(csv_reader)

                # Process each row
                for row in csv_reader:
                    your_name, your_email, your_phone, company_name, Date = row

                    # Parse the date
                    date = timezone.datetime.strptime(Date, "%m/%d/%y, %I:%M%p")

                    # Fetch or create related objects
                    # source, _ = Source.objects.get_or_create(name="Website")  # Assuming the source is "Website"
                    sub_source = None  # If sub_source is derived from somewhere, handle it accordingly

                    # Create the Lead object with status=None
                    Lead.objects.create(
                        date=date,
                        company_name=company_name,
                        phone_number=your_phone,
                        email=your_email,
                        source=None,
                        sub_source=sub_source,
                        point_of_contact=your_name,
                        lead_status=None  # If lead_status can be derived from other fields, handle it accordingly
                    )

                return Response({'status': 'file processed'}, status=status.HTTP_201_CREATED)                    
            else:
                return Response({'error': 'Invalid processing_type'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_valid_file_type(self, file):
        # Check file extension
        valid_extensions = ['.csv', '.xls', '.xlsx']  # Add valid file extensions here
        _, file_extension = os.path.splitext(file.name)
        return file_extension.lower() in valid_extensions


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Lead
from django.db import models


@receiver(post_save, sender=Lead)
def assign_lead_to_user(sender, instance, created, **kwargs):
    if created and not instance.assigned:
        # Get all active users
        active_users = User.objects.filter(is_active=True)
        
        # Get the index of the last assigned user
        last_assigned_index = Lead.objects.aggregate(models.Max('assigned'))['assigned__max']

        # Calculate the index of the next user to be assigned in round-robin manner
        next_assigned_index = (last_assigned_index + 1) % len(active_users)

        # Get the next user to be assigned
        next_user = active_users[next_assigned_index]

        # Assign the lead to the next user in round-robin
        instance.assigned = next_user
        instance.save()