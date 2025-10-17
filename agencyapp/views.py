from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from framework_core.permissions import IsAgencyUserRole
from agencyapp.serializers import AgencyProfileSerializer

class AgencyProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
        This class allows to have GET logged in user, PUT/PATCH logged in user info,
        allows deactivating user with DELETE (RetrieveUpdateAPIView, & RetrieveUpdateDestroyAPIView)
    """
    serializer_class = AgencyProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgencyUserRole]

    def get_object(self):
        # always return logged in user for authorization
        return self.request.user
    
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # validation before serializer
        # if 'company_name' in request.data:
        #     new_name = request.data['company_name']
        #     if len(new_name) < 3:
        #         raise ValidationError({'company_name': 'Company name must be at least 3 characters long.'})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # validaion afer serializer and before perform update
        # if serializer.validated_data.get('address') == 'invalid':
        #     raise ValidationError({'address': 'Invalid address provided.'})

        self.perform_update(serializer)

        email = serializer.data.get('email')
        user_id = serializer.data.get('id')
        is_active = serializer.data.get('is_active')

        return Response({
            'message': 'User updated successfully',
            'account_info': {
                'id': str(user_id),
                'email': email,
                'is_active': is_active
            }
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({
            'message': 'User deactivated successfully',
            'account_info': {
                'id': str(user.id),
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
        }, status=status.HTTP_200_OK)

class AgencyDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAgencyUserRole]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'company_name': user.company_name,
            'email': user.email,
            'address': user.address,
            'contact_details': user.contact_details,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
            'role': user.role
        }

        return Response({'agency_summary': data})