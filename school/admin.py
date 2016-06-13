from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import Promotion, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'promotion', 'graduate')
    search_fields = ('number', 'user__first_name', 'user__last_name')

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

admin.site.register(Promotion)
admin.site.register(Student, StudentAdmin)
