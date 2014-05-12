from django.contrib import admin

from django_markdown.admin import MarkdownModelAdmin

from .models import Promotion, Student

class StudentAdmin(MarkdownModelAdmin):
    list_display = ('user', 'number', 'promotion', 'nickname')
    search_fields = ('number', 'user__first_name', 'user__last_name')
    
admin.site.register(Promotion)
admin.site.register(Student, StudentAdmin)