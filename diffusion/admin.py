from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Place, Award, MetaAward


class AwardAdmin(admin.ModelAdmin):
    list_display = ('get_year', 'get_award', 'get_artwork')
    search_fields = ['meta_award__label', 'artwork__title', 'artwork__authors__user__last_name']
    ordering = ['date']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def get_year(self, obj):
        return obj.date.year
    get_year.short_description = "Annee"
    get_year.admin_order_field = 'date'

    def get_award(self, obj):
        return obj.meta_award.label
    get_award.short_description = "Titre"
    get_award.admin_order_field = 'meta_award__label'

    def get_artwork(self, obj):
        return ", ".join([artwork.__unicode__() for artwork in obj.artwork.all()])
    get_artwork.short_description = "Oeuvre(s)"
    get_artwork.admin_order_field = 'artwork'


class PlaceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class MetaAwardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(Place, PlaceAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(MetaAward, MetaAwardAdmin)
