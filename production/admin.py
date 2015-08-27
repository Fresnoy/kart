from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Production, FilmGenre, Film, InstallationGenre, Installation, Performance, StaffTask, OrganizationTask, Event, Itinerary

class CollaboratorsInline(admin.TabularInline):
    model = Production.collaborators.through

class PartnersInline(admin.TabularInline):
    model = Production.partners.through

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ['title']
    inlines = (CollaboratorsInline, PartnersInline)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

class ArtworkAdmin(ProductionAdmin):
    list_display = (ProductionAdmin.list_display + ('production_date',))
    filter_horizontal = ('authors', 'beacons')

@admin.register(Event)
class EventAdmin(ProductionAdmin):
    list_display = (ProductionAdmin.list_display + ('starting_date', 'ending_date'))

class ItineraryArtworkInline(admin.TabularInline):
    model = Itinerary.artworks.through

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    inlines = (ItineraryArtworkInline,)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

@admin.register(FilmGenre)
class FilmGenreAdmin(admin.ModelAdmin):
    pass

@admin.register(InstallationGenre)
class InstallationGenreAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationTask)
class OrganizationTaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

@admin.register(StaffTask)
class StaffTaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }
