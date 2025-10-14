from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.save()

            return Response({
                "message": "User Created Successfully",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "role": user.role,
                    "date_joined": user.date_joined
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error", "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_200_OK
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "message": "Login Successful",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(access)
            }
        }, status=status.HTTP_200_OK)
