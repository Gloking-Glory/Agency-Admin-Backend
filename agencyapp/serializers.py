from rest_framework import serializers
from userapp.models import User

class AgencyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'company_name', 'address', 'contact_details', 'is_active']
        read_only_fields = ['id', 'email', 'is_active']
    
    # validation in serializer
    # def validate_company_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError('Company name must be at least 3 characters long.')
    #     return value

    def validate(self, attrs):
        company_name = attrs.get('company_name')
        address = attrs.get('address')

        if not company_name:
            raise serializers.ValidationError('Company name is required')
        if not address:
            raise serializers.ValidationError('Address is required')

        return attrs
