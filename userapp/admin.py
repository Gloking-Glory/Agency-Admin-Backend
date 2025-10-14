from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_dispaly = ('email', 'role', 'address', 'company_name', 'contact_details', 'is_active', 'created_date'),
    search_fields = ('email', 'role', 'company_name')
    list_filter = ('email', 'is_active')
    ordering = ('-date_joined',)
