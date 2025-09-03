from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.utils.html import format_html

from people.forms import UserCreateForm
from people.models import Artist, FresnoyProfile, Staff, Organization

from guardian.admin import GuardedModelAdmin


class ArtistAdmin(admin.ModelAdmin):
    """Admin model for Artist."""

    list_display = ('nick',)
    search_fields = [
        'user__first_name',
        'user__last_name',
        'nickname',
    ]
    # filter_horizontal = ('websites', 'collectives')
    readonly_fields = ('artist_photo_picture',)
    # list fields order the picture after artist_photo
    fields = (
        'user',
        'collectives',
        'nickname',
        'alphabetical_order',
        'artist_photo',
        'artist_photo_picture',
        'artist_photo_copyright',
        'bio_short_fr',
        'bio_short_en',
        'bio_fr',
        'bio_en',
        'twitter_account',
        'facebook_profile',
        'websites',
    )
    raw_id_fields = ('user', 'collectives', 'websites')
    autocomplete_lookup_fields = {'fk': ['user'], 'm2m': ['collectives', 'websites']}

    def nick(self, obj):
        # user can be None
        if obj.user:
            if obj.nickname != "":
                return "{} ({} {})".format(obj.nickname, obj.user.first_name, obj.user.last_name)
            else:
                return "{} {}".format(obj.user.first_name, obj.user.last_name)
        # User None
        if obj.nickname != "":
            return obj.nickname
        return "???"

    # describe 'nick'
    nick.short_description = 'Nick name (real name if any) or real name'

    def firstname(self, obj):
        return obj.user.first_name

    def lastname(self, obj):
        return obj.user.last_name

    def artist_photo_picture(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.artist_photo.url))


class FresnoyProfileInline(admin.StackedInline):
    """StackedInline admin for FresnoyProfile."""

    model = FresnoyProfile
    readonly_fields = (
        'is_artist',
        'is_student',
        'is_staff',
    )


class FresnoyProfileAdmin(UserAdmin):
    """Admin for Use and additionnal profile fields."""

    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    add_form = UserCreateForm
    add_fieldsets = (
        (
            None,
            {
                'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email'),
            },
        ),
    )
    ordering = ('first_name',)


class StaffAdmin(GuardedModelAdmin):
    search_fields = ['user__username', 'user__last_name', 'user__first_name', 'user__artist__nickname']
    list_display = (
        "name",
        "artist",
    )
    raw_id_fields = ('user',)
    autocomplete_lookup_fields = {
        'fk': ['user'],
    }

    def artist(self, obj):
        return obj.user.profile.is_artist

    def name(self, obj):
        return obj.__str__()


class OrganizationAdmin(GuardedModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    ordering = ('name',)


def user_unicode(self):
    return '{0} {1}'.format(self.first_name.title(), self.last_name.title())


User.__str__ = user_unicode

admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Organization, OrganizationAdmin)
