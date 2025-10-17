from rest_framework import serializers
from userapp.models import User

class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'company_name', 'address', 'contact_details', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']

class AdminEditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'email', 'company_name', 'address', 'contact_details', 'is_active']
        extra_kwargs = {
            'role': { 'required': True },
            'email': { 'required': True },
            'company_name': { 'required': True },
            'address': { 'required': True },
            'contact_details': { 'required': True },
            'is_active': { 'required': True }
        }

    def validate(self, attrs):
        email = attrs.get('email')
        if email and not email.endswith('.com'):
            raise serializers.ValidationError({
                'email': 'Email must end with .com'
            })
        return attrs
