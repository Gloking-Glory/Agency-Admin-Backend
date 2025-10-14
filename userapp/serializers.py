from rest_framework import serializers
from userapp.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[choice[0] for choice in User._meta.get_field('role').choices], # pylint: disable=no-member, protected-access
        required=True,
        error_messages={
            "required": 'Role is required',
            "invalid_choice": 'Invalid role type'
        }
    )

    password = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True,
        error_messages={
            "required": 'Password is required',
            "min_length": 'Password must be at least 6 characters long'
        }
    )

    class Meta:
        model = User
        fields = ["id", "role", "email", "company_name", "address", "contact_details", "password", "date_joined"]
        extra_kwargs = {
            'password': { 'write_only': True },
            'company_name': { 'required': False, 'allow_blank': True },
            'address': { 'required': False, 'allow_blank': True },
            'contact_details': { 'required': False, 'allow_blank': True }
        }

    def validate(self, attrs):
        role = attrs.get('role')

        if role == 'AGENCY':
            missing_fields = []

            if not attrs.get("company_name"):
                missing_fields.append("company_name")
            if not attrs.get("address"):
                missing_fields.append("address")
            
            if missing_fields:
                raise serializers.ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs

        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
