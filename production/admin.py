from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import Production, Artwork, FilmGenre, Film, InstallationGenre, Installation, Performance, StaffTask, OrganizationTask, Event, Itinerary


class CollaboratorsInline(admin.TabularInline):
    model = Production.collaborators.through


class PartnersInline(admin.TabularInline):
    model = Production.partners.through


class ProductionChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Production

class ArtworkChildAdmin(ProductionChildAdmin):
    base_model = Artwork
    list_display = (ProductionChildAdmin.list_display + ('production_date',))
    filter_horizontal = ('authors', 'beacons')


class FilmChildAdmin(ArtworkChildAdmin):
    pass


class PerformanceChildAdmin(ArtworkChildAdmin):
    pass

class InstallationChildAdmin(ArtworkChildAdmin):
    pass


# @admin.register(Production)
class ProductionParentAdmin(PolymorphicParentModelAdmin):
    list_display = ('title', 'subtitle')
    search_fields = ['title']
    inlines = (CollaboratorsInline, PartnersInline)

    base_model = Production
    child_models = (
        (Film, FilmChildAdmin),
        (Installation, InstallationChildAdmin),
        (Performance, PerformanceChildAdmin),
    )


    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    base_model = Installation

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    base_model = Film

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    base_model = Performance



@admin.register(Event)
class EventAdmin(ProductionChildAdmin):
    list_display = (ProductionChildAdmin.list_display + ('starting_date', 'ending_date'))


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

