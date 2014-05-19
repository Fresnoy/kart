from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django_markdown.admin import MarkdownModelAdmin

from .forms import UserCreateForm
from .models import Artist, Staff, FresnoyProfile, Organization

class ArtistAdmin(MarkdownModelAdmin):
    list_display = ('user', 'nickname')
    filter_horizontal = ('websites',)    

class FresnoyProfileInline(admin.StackedInline):
    model = FresnoyProfile
    max_num = 1
    can_delete = False

class FresnoyProfileAdmin(UserAdmin):
    inlines = (FresnoyProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    add_form = UserCreateForm

    add_fieldsets = ((None, {'fields':('username','password1','password2','first_name','last_name','email'),}),)    

admin.site.unregister(User)
admin.site.register(User, FresnoyProfileAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff)
admin.site.register(Organization)