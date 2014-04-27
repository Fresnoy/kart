from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from people.api import ArtistResource, StaffResource
from production.api import InstallationResource, FilmResource, EventResource, ExhibitionResource, ItineraryResource, ArtworkResource
from diffusion.api import PlaceResource
from school.api import PromotionResource, StudentResource


v1_api = Api(api_name='v1')
v1_api.register(InstallationResource())
v1_api.register(FilmResource())
v1_api.register(EventResource())
v1_api.register(PromotionResource())
v1_api.register(StudentResource())
v1_api.register(ArtistResource())
v1_api.register(StaffResource())
v1_api.register(PlaceResource())
v1_api.register(ExhibitionResource())
v1_api.register(ItineraryResource())
v1_api.register(ArtworkResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ifresnoy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^', include(v1_api.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
    url(r'v1/doc/',
      include('tastypie_swagger.urls', namespace='ifresnoy_tastypie_swagger'),
      kwargs={"tastypie_api_module":"ifresnoy.urls.v1_api", "namespace":"ifresnoy_tastypie_swagger"}
    ),                       
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)