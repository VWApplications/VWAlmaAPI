from django.contrib import admin
from django.contrib.auth import get_user_model

# Get the custom user from settings
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """
    New admin user form configuration.
    """

    list_display = ['name', 'email', 'created_at']
    search_display = ['name', 'email']
    list_filter = ['created_at', 'is_staff']


# Create models on django admin
admin.site.register(User, UserAdmin)
