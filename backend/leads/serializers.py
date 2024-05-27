from rest_framework import serializers
from core.models import Lead,Source,SubSource, Status


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class SubSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSource
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    processing_type = serializers.ChoiceField(choices=[('0', 'Custom Format'), ('1', 'Facebook'),('2','Website')], default='0')


class LeadSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), required=True)
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Lead
        fields = '__all__'

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')

        # Ensure at least one of phone_number or email is provided
        if not phone_number and not email:
            raise serializers.ValidationError("Either phone number or email is required.")

        return attrs

    def get_fields(self):
        fields = super().get_fields()
        # Set required=False for all fields except company_name, source, phone_number, and email and date
        for field_name in fields:
            if field_name not in ['date', 'source', 'phone_number', 'email']:
                fields[field_name].required = False
        return fields