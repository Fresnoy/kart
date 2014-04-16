from django.contrib import admin

from .models import Artist, Staff

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Staff)