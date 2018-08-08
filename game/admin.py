from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'is_staff')
    inlines = (ProfileInline,)

    # def get_elo(self, instance):
    #     return instance.profile.elo
    # get_elo.short_description = 'Elo'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Profile)
