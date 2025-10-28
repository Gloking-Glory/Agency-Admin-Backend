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


# customizing the response in seriazlizer
    # def create(self, validated_data):
    #     course = Course.objects.create(**validated_data)
    #     # ✅ Return a clean response shape if you want a custom message (not required, but possible)
    #     self.context["custom_message"] = "Course created successfully"
    #     return course

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     self.context["custom_message"] = "Course updated successfully"
    #     return instance

# the view instance
# from rest_framework import generics, status
# from rest_framework.response import Response
# from .serializers import CourseSerializer

# class CourseViewSet(generics.CreateAPIView):
#     serializer_class = CourseSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         course = serializer.save()

#         message = serializer.context.get("custom_message", "Course created")

#         return Response({
#             "message": message,
#             "data": serializer.data
#         }, status=status.HTTP_201_CREATED)


# user confirm deletion, yes or no before delete serializer
# class CourseDeleteConfirmSerializer(serializers.Serializer):
#     confirm = serializers.BooleanField()

#     def validate_confirm(self, value):
#         if not value:
#             raise serializers.ValidationError("You must confirm deletion.")
#         return value
