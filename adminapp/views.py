from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from framework_core.permissions import IsAdminUserRole
from adminapp.serializers import AdminUserListSerializer, AdminEditUserSerializer
from framework_core.pagination import PagePagination
from userapp.models import User
from django.utils import timezone
# from rest_framework.exceptions import PermissionDenied

class AdminUserListView(generics.ListAPIView):
    # admin -- list and search for all users ---- GET /api/admin/users/
    serializer_class = AdminUserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]
    pagination_class = PagePagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'role', 'email', 'company_name', 'is_active']
    ordering_fields = ['date_joined', 'is_active', 'role']

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')

        if role:
            queryset = queryset.filter(role=role)

        return queryset.order_by('-date_joined')

class AdminEditUserView(generics.RetrieveUpdateAPIView):
    # admin -- edit user info ---- GET/PUT/PATCH /api/admin/users/<id>/
    serializer_class = AdminEditUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]
    queryset = User.objects.all()
    lookup_field = 'id'

    # perform update restriction
    # def perform_update(self, serializer):
    #     user = self.get_object()
    #     if user.role == 'ADMIN' and not self.request.user.is_superuser:
    #         raise PermissionDenied("You cannot modify another admin")
    #     serializer.save()


class AdminDeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]
    queryset = User.objects.all()
    lookup_field = 'id'

    # perfrom destroy restriction
    # def perform_destroy(self, instance):
    #     if instance.role == 'ADMIN':
    #         raise ValidationError("Cannot delete an admin account")
    #     instance.is_active = False
    #     instance.save()

    # customize delete response
    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response({"detail": "User deleted successfully"}, status=200)


class AdminSummaryView(APIView):
    # returns total counts of users by role --- GET /api/admin/summary
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        today = timezone.now().date()
        total_users = User.objects.count()
        total_agencies = User.objects.filter(role='AGENCY').count()
        total_admins = User.objects.filter(role='ADMIN').count()
        date_added = User.objects.filter(date_joined__date=today).count()

        return Response({
            'total_users': total_users,
            'total_agencies': total_agencies,
            'total_admins': total_admins,
            'date_added': date_added
        })
