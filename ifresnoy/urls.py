from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from production.api import InstallationResource

v1_api = Api(api_name='v1')
v1_api.register(InstallationResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ifresnoy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^', include(v1_api.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
