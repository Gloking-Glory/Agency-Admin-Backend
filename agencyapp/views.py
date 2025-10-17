from rest_framework import generics, permissions
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

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})

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