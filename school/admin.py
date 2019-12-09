# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Promotion, Student, StudentApplication, StudentApplicationSetup


class StudentAdmin(admin.ModelAdmin):
    list_display = ('artist', 'number', 'promotion', 'graduate')
    search_fields = ('number', 'user__first_name', 'user__last_name')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class StudentApplicationAdmin(admin.ModelAdmin):

    def _get_name(self, obj):
        return obj.artist.user.get_full_name()

    _get_name.short_description = "Nom"
    list_display = (
        'campaign',
        '_get_name',
        'current_year_application_count',
        'selected_for_interview',
        'selected',
        'remark',
    )


class StudentApplicationSetupAdmin(admin.ModelAdmin):

    def _get_name(self, obj):
        return obj.artist.user.get_full_name()

    list_display = (
        'name',
        'is_current_setup',
    )


admin.site.register(Promotion)
admin.site.register(StudentApplication, StudentApplicationAdmin)
admin.site.register(StudentApplicationSetup, StudentApplicationSetupAdmin)
admin.site.register(Student, StudentAdmin)
