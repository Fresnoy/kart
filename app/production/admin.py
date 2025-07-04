from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget
from polymorphic.admin import PolymorphicChildModelAdmin

from .models import (
    Production, Artwork, FilmGenre, Film,
    InstallationGenre, Installation, Performance,
    StaffTask, OrganizationTask, Event, Itinerary)


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


class FilmChildAdmin(ArtworkChildAdmin, admin.ModelAdmin):
    pass


class PerformanceChildAdmin(ArtworkChildAdmin):
    pass


class InstallationChildAdmin(ArtworkChildAdmin):
    pass


@admin.register(Production)
class ProductionParentAdmin(PolymorphicChildModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'subtitle',)
    search_fields = ['title']
    inlines = (CollaboratorsInline, PartnersInline)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    base_model = Production
    child_models = (
        (Film, FilmChildAdmin),
        (Installation, InstallationChildAdmin),
        (Performance, PerformanceChildAdmin),
    )


class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'get_diffusions', 'get_awards')
    search_fields = ['title', ]
    inlines = (CollaboratorsInline, PartnersInline)
    filter_vertical = ('authors', 'beacons',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def get_authors(self, obj):
        return ", ".join([author.__str__() for author in obj.authors.all()])
    get_authors.short_description = "Artist(s)"

    def get_diffusions(self, obj):
        return ", ".join([event.__str__() for event in obj.events.all()])
    get_diffusions.short_description = "Diffusion(s)"
    get_diffusions.admin_order_field = 'events'

    def get_awards(self, obj):
        return ", ".join(['{0} {1} ({2})'.format(award.meta_award.label, award.date.year, award.meta_award.event.title)
                         for award in obj.award.all()])
    get_awards.short_description = "Award(s)"
    get_awards.admin_order_field = 'award'


@admin.register(Installation)
class InstallationAdmin(ArtworkAdmin):
    base_model = Installation


@admin.register(Film)
class FilmAdmin(ArtworkAdmin):
    base_model = Film
    filter_vertical = ('shooting_place', )


@admin.register(Performance)
class PerformanceAdmin(ArtworkAdmin):
    base_model = Performance


@admin.register(Event)
class EventAdmin(ProductionChildAdmin):
    show_in_index = True
    list_display = (ProductionChildAdmin.list_display + ('starting_date', 'type', 'main_event'))
    search_fields = ['title', 'parent_event__title']
    inlines = (CollaboratorsInline, PartnersInline)
    filter_vertical = ('subevents', "films", "installations", "performances")

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def get_ordering(self, request):
        return ['id']  # sort case insensitive


class ItineraryArtworkInline(admin.TabularInline):
    model = Itinerary.artworks.through


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    search_fields = ['label_fr', 'event__title']
    inlines = (ItineraryArtworkInline,)

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
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
        models.TextField: {'widget': AdminPagedownWidget},
    }
    ordering = ('label',)


@admin.register(StaffTask)
class StaffTaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    ordering = ('label',)
