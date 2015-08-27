from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Place, Award

class AwardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

class PlaceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }


admin.site.register(Place, PlaceAdmin)
admin.site.register(Award, AwardAdmin)
