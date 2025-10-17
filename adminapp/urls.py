from django.urls import path
from .views import AdminUserListView, AdminEditUserView, AdminDeleteUserView, AdminSummaryView

urlpatterns = [
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('edit-user/<uuid:id>/', AdminEditUserView.as_view(), name='admin-edit-user'),
    path('delete-user/<uuid:id>/delete/', AdminDeleteUserView.as_view(), name='admin-delete-user'),
    path('summary/', AdminSummaryView.as_view(), name='admin-summary')
]
