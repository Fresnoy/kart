from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Artist, Staff, FresnoyProfile


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')

class FresnoyProfileInline(admin.StackedInline):
    model = FresnoyProfile
    max_num = 1
    can_delete = False

class FresnoyProfileAdmin(UserAdmin):
    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff)