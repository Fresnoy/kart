# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Promotion, Student, StudentApplication

import csv
from django.http import HttpResponse

class StudentAdmin(admin.ModelAdmin):
    list_display = ('artist', 'number', 'promotion', 'graduate')
    search_fields = ('number', 'user__first_name', 'user__last_name')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

def output_excel(modeladmin, request, queryset):
    # do something

    response = HttpResponse()
    response['content_type'] = 'text/csv;'
    response['mime_type'] = 'text/csv;'
    response['Content-Disposition'] = 'attachment; filename="candidats_concours.csv"'
    response.write(u'\ufeff'.encode('utf8'))


    writer = csv.writer(response)
    writer.writerow(['Soumission du dossier', 'Nom', 'Prénom', 'N.Dossier', 'Sexe', 'Date de Naissance', 'Nationalité', 'Email','Adresse postale', 'Matériel', 'oral', 'Note finale', 'SKYPE', 'note sélection 2', 'note sélection 3', 'diplôme'])

    for obj in queryset:
        writer.writerow([obj.updated_on, obj.artist.user.last_name,  obj.artist.user.first_name, obj.current_year_application_count, '', '', '', obj.artist.user.email  ])


    return response
    
output_excel.short_description = "Sortie Excel"



class StudentApplicationAdmin(admin.ModelAdmin):
    actions = [output_excel]

    def _get_name(self,obj):
        return obj.artist.user.get_full_name()

    _get_name.short_description = "Nom"
    list_display = ('_get_name','current_year_application_count','created_on','selected_for_interview')





admin.site.register(Promotion)
admin.site.register(StudentApplication, StudentApplicationAdmin )
admin.site.register(Student, StudentAdmin)
