from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profile.models import Otp, Industry, Domain, Function, Profile, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['industry', 'domain', 'function', 'career_stage', 'Organization_Size', 'countries']
    autocomplete_fields = ('domain',)
    exclude = ['industry']

    def save_model(self, request, obj, form, change):
        domain = obj.domain
        industry = domain.industry
        obj.industry = industry
        obj.save()
        super().save_model(request, obj, form, change)


class DomainAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class CustomUserAdmin(UserAdmin):
    """Custom user admin."""
    ordering = ['username']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Otp)
admin.site.register(Industry)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Function)
admin.site.register(Profile, ProfileAdmin)


