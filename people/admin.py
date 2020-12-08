from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from people.forms import UserCreateForm
from people.models import Artist, FresnoyProfile, Staff, Organization

from guardian.admin import GuardedModelAdmin


class ArtistAdmin(admin.ModelAdmin):
    """ Admin model for Artist.
    """
    list_display = ('nick',)
    search_fields = ['user__first_name', 'user__last_name']
    filter_horizontal = ('websites',)

    def nick(self, obj):
        return ("{} ({} {})".format(obj.nickname,
                                    obj.user.first_name,
                                    obj.user.last_name) if obj.nickname
                else "{} {}".format(obj.user.first_name, obj.user.last_name))
    nick.short_description = 'Nick name (real name) or real name'

    def firstname(self, obj):
        return obj.user.first_name

    def lastname(self, obj):
        return obj.user.last_name


class FresnoyProfileInline(admin.StackedInline):
    """StackedInline admin for FresnoyProfile.
    """
    model = FresnoyProfile
    readonly_fields = ('is_artist', 'is_student', 'is_staff',)


class FresnoyProfileAdmin(UserAdmin):
    """ Admin for Use and additionnal profile fields.
    """
    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    add_form = UserCreateForm
    add_fieldsets = ((None, {'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email'), }), )


class StaffAdmin(GuardedModelAdmin):
    search_fields = ['user__username', 'user__last_name', 'user__first_name']
    list_display = ("user", "artist")

    def artist(self, obj):
        return obj.user.profile.is_artist


class OrganizationAdmin(GuardedModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    ordering = ('name',)


def user_unicode(self):
    return '{0} {1}'.format(self.first_name.capitalize(), self.last_name.capitalize())


User.__str__ = user_unicode

admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Organization, OrganizationAdmin)
