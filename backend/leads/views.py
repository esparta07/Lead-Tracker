import csv
from io import StringIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .serializers import FileUploadSerializer,LeadSerializer,SourceSerializer, SubSourceSerializer, StatusSerializer
from core.models import Lead, User, Source, SubSource,Source, SubSource, Status
from drf_spectacular.utils import extend_schema

from django.core.exceptions import ValidationError
import os

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
                # For processing_type '1', do nothing for now
                return Response({'status': 'file processing for type 1 not implemented'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid processing_type'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_valid_file_type(self, file):
        # Check file extension
        valid_extensions = ['.csv', '.xls', '.xlsx']  # Add valid file extensions here
        _, file_extension = os.path.splitext(file.name)
        return file_extension.lower() in valid_extensions

