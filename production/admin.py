from django.contrib import admin

from .models import Production, Film, Installation, Performance, StaffTask, OrganizationTask, Event

class CollaboratorsInline(admin.TabularInline):                                                                                               
    model = Production.collaborators.through

class PartnersInline(admin.TabularInline):                                                                                               
    model = Production.partners.through   

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    inlines = (CollaboratorsInline, PartnersInline)
    
class ArtworkAdmin(ProductionAdmin):
    list_display = (ProductionAdmin.list_display + ('production_date',))
    filter_horizontal = ('process_galleries', 'mediation_galleries', 'in_situ_galleries', 'authors')

class EventAdmin(ProductionAdmin):
    list_display = (ProductionAdmin.list_display + ('starting_date', 'ending_date'))

# Tasks
admin.site.register(OrganizationTask)
admin.site.register(StaffTask)

# Artworks
admin.site.register(Film, ArtworkAdmin)
admin.site.register(Installation, ArtworkAdmin)
admin.site.register(Performance, ArtworkAdmin)

# Events
admin.site.register(Event, EventAdmin)

