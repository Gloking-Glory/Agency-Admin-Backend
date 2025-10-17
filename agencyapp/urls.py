from django.urls import path
from .views import AgencyProfileView, AgencyDashboardView

urlpatterns = [
    path('agency-profile/', AgencyProfileView.as_view(), name='agency-profile'),
    path('agency-dashboard/', AgencyDashboardView.as_view(), name='agency-dashboard')
]
