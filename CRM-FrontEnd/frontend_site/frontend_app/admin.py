# admin.py
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'employee_id', 'position', 'city', 'country')  # Fields to display in the admin panel
    search_fields = ('first_name', 'last_name', 'email')  # Enable search by fields
    list_filter = ('city', 'country')  # Enable filtering by city and country

admin.site.register(UserProfile, UserProfileAdmin)
