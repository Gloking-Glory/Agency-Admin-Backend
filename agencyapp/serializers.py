from rest_framework import serializers
from userapp.models import User

class AgencyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'company_name', 'address', 'contact_details', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']

    def validate(self, attrs):
        company_name = attrs.get('company_name')
        address = attrs.get('address')

        if not company_name:
            raise serializers.ValidationError('Company name is required')
        if not address:
            raise serializers.ValidationError('Address is required')

        return attrs
