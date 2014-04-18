from django.contrib import admin

from .models import Film, Installation, Performance

class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'production_date')
    filter_horizontal = ('process_galleries', 'mediation_galleries', 'in_situ_galleries', 'authors')

    
admin.site.register(Film, ArtworkAdmin)
admin.site.register(Installation, ArtworkAdmin)
admin.site.register(Performance, ArtworkAdmin)

