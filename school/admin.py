from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Promotion, Student, StudentApplication

class StudentAdmin(admin.ModelAdmin):
    list_display = ('artist', 'number', 'promotion', 'graduate')
    search_fields = ('number', 'user__first_name', 'user__last_name')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ('artist', 'selected_for_interview', 'updated_on')



admin.site.register(Promotion)
admin.site.register(StudentApplication, StudentApplicationAdmin )
admin.site.register(Student, StudentAdmin)
