from django.contrib import admin

from django_markdown.admin import MarkdownModelAdmin

from .models import Place, Award

admin.site.register(Place, MarkdownModelAdmin)
admin.site.register(Award, MarkdownModelAdmin)

