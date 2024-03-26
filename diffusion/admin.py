from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

from pagedown.widgets import AdminPagedownWidget

from .models import Place, Award, MetaAward, MetaEvent, Diffusion


class AwardAdmin(admin.ModelAdmin):
    list_display = ('get_year', 'get_award', 'get_artwork')
    search_fields = ['meta_award__label', 'artwork__title',
                     'artwork__authors__user__last_name']
    ordering = ['date']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def get_year(self, obj):
        return obj.date.year if obj.date else None

    get_year.short_description = "Annee"
    get_year.admin_order_field = 'date'

    def get_award(self, obj):
        return obj.meta_award.label if obj.meta_award else None

    get_award.short_description = "Titre"
    get_award.admin_order_field = 'meta_award__label'

    def get_artwork(self, obj):
        return ", ".join([artwork.__str__() for artwork in obj.artwork.all()])

    get_artwork.short_description = "Oeuvre(s)"
    get_artwork.admin_order_field = 'artwork'

    # order manytomany artist field
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "artist":
            kwargs["queryset"] = User.objects.order_by('first_name')
        return super(admin.ModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'city', 'country']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class MetaEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'genres', 'keywords_list', 'get_periode')
    search_fields = ['event__title', 'event__starting_date']
    ordering = ['event', ]

    def keywords_list(self, obj):
        return u", ".join(o.name for o in obj.keywords.all())

    def get_periode(self, obj):
        return obj.event.starting_date.strftime("%B")
    get_periode.short_description = 'Periode'


class MetaAwardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class DiffusionAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'event', 'first', 'on_competition')
    ordering = ['artwork', ]


admin.site.register(Place, PlaceAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(MetaAward, MetaAwardAdmin)
admin.site.register(MetaEvent, MetaEventAdmin)
admin.site.register(Diffusion, DiffusionAdmin)
