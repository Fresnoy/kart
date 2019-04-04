from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from people.forms import UserCreateForm
from people.models import Artist, FresnoyProfile




class FresnoyProfileInline(admin.StackedInline):
    model = FresnoyProfile


class ArtistAdmin(admin.ModelAdmin):
    """ Admin model for Artist.
    """
    list_display = ('nick','firstname')
    search_fields = ['user__first_name', 'user__last_name']
    filter_horizontal = ('websites',)
    
    def nick(self, obj):
        return "{} ({} {})".format(obj.nickname, obj.user.first_name,obj.user.last_name)

    def firstname(self, obj):
            return obj.user.first_name

    def lastname(self, obj):
        return obj.user.last_name


class FresnoyProfileAdmin(UserAdmin):
    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    add_form = UserCreateForm
    add_fieldsets = ((None, {'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email'), }), )



admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
