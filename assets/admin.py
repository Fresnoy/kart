from django.contrib import admin

from .models import Gallery, Medium

class MediumAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'picture', 'medium_url')

class MediumInline(admin.TabularInline):
    model = Medium

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    exclude = ('media',)
    inlines = (MediumInline,)


admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(Medium, MediumAdmin)
