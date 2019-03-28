from django.contrib import admin

from .models import FresnoyProfile
from people.models import Artist

admin.site.register(FresnoyProfile)
admin.site.register(Artist)
