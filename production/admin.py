from django.contrib import admin

from .models import Film, Installation, Event

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'production_date')
    filter_horizontal = ('galleries', 'authors')

    
admin.site.register(Film, ProductionAdmin)
admin.site.register(Installation, ProductionAdmin)
admin.site.register(Event, ProductionAdmin)

