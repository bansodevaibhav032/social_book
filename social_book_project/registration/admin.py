from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'get_age', 'public_visibility', 'address', 'is_staff', 'is_active',)
    def get_age(self, obj):
        return obj.age()
    get_age.short_description = 'Age'
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'get_age', 'public_visibility', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'get_age', 'public_visibility', 'address'),
        }),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)

# Register the custom admin for CustomUser
admin.site.register(CustomUser, CustomUserAdmin)


