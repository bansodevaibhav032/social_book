from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'age', 'birth_year', 'address', 'is_verified', 'public_visibility', 'is_staff', 'is_active',)
    search_fields = ('email', )
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email',  'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'age', 'birth_year', 'address', 'is_verified', 'public_visibility')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', 'is_staff', 'is_active', 'age', 'birth_year', 'address', 'is_verified', 'public_visibility'),
        }),
    )

    def get_token(self, obj):
        return obj.get_token()

    get_token.short_description = 'Access Token'

    # For regular users only
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

    # For superusers only
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(is_superuser=True)

# Register the custom admin for CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFile)
