from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

from pagedown.widgets import AdminPagedownWidget
from guardian.admin import GuardedModelAdmin

from .forms import UserCreateForm
from .models import Artist, Staff, FresnoyProfile, Organization


class ArtistAdmin(GuardedModelAdmin):
    list_display = ('firstname', 'lastname', 'nickname')
    filter_horizontal = ('websites',)
    search_fields = ['user__first_name', 'user__last_name']

    def firstname(self, obj):
        return obj.user.first_name

    def lastname(self, obj):
        return obj.user.last_name

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class FresnoyProfileInline(admin.StackedInline):
    model = FresnoyProfile
    max_num = 1
    can_delete = False


class FresnoyProfileAdmin(UserAdmin):
    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    add_form = UserCreateForm

    add_fieldsets = ((None, {'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email'), }), )


admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff)
admin.site.register(Organization)
