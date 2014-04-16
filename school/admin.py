from django.contrib import admin

from .models import Promotion, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'promotion', 'nickname')
    search_fields = ('number', 'user__first_name', 'user__last_name')
    
admin.site.register(Promotion)
admin.site.register(Student, StudentAdmin)