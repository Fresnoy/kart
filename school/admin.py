# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Promotion, Student, StudentApplication

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class StudentAdmin(admin.ModelAdmin):
    list_display = ('artist', 'number', 'promotion', 'graduate')
    search_fields = ('number', 'user__first_name', 'user__last_name')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }


def output_excel(modeladmin, request, queryset):
    # do something
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


output_excel.short_description = "Sortie Excel"



class StudentApplicationAdmin(admin.ModelAdmin):

    def _get_name(self,obj):
        return obj.artist.user.get_full_name()

    _get_name.short_description = "Nom"
    list_display = ('_get_name','current_year_application_count','created_on','selected_for_interview')




admin.site.register(Promotion)
admin.site.register(StudentApplication, StudentApplicationAdmin )
admin.site.register(Student, StudentAdmin)
