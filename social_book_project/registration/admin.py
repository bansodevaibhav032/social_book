from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import UploadedFile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email',  'age', 'birth_year', 'address', 'public_visibility', 'is_staff', 'is_active',)
    search_fields = ('email', )
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email',  'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'age', 'birth_year', 'address', 'public_visibility')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', 'is_staff', 'is_active', 'age', 'birth_year', 'address', 'public_visibility'),
        }),
    )

    #for Users Only
    # def get_queryset(self, request):
    #     # Override get_queryset to filter users in the list view
    #     qs = super().get_queryset(request)
    #     return qs.filter(is_superuser=False)
    
    #for SuperUseronly
    # def get_queryset(self, request):
    #     # Override get_queryset to filter users in the list view
    #     qs = super().get_queryset(request)
    #     return qs.filter(is_superuser=True)
# Register the custom admin for CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFile)
