from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from people.api import ArtistResource, StaffResource
from production.api import (
    InstallationResource, FilmResource,
    PerformanceResource, EventResource, ExhibitionResource,
    ItineraryResource, ArtworkResource
)
from diffusion.api import PlaceResource
from school.api import PromotionResource, StudentResource, StudentApplicationResource

from people.views import (
    ArtistViewSet, UserViewSet, FresnoyProfileViewSet,
    StaffViewSet, OrganizationViewSet
)
from school.views import (
    PromotionViewSet, StudentViewSet,
    StudentAutocompleteSearchViewSet, StudentApplicationViewSet
)
from production.views import (
    FilmViewSet, InstallationViewSet,
    PerformanceViewSet, FilmGenreViewSet,
    InstallationGenreViewSet, EventViewSet,
    ItineraryViewSet,
    CollaboratorViewSet, PartnerViewSet
)
from diffusion.views import PlaceViewSet
from common.views import BTBeaconViewSet, WebsiteViewSet
from assets.views import GalleryViewSet, MediumViewSet


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(InstallationResource())
v1_api.register(FilmResource())
v1_api.register(PerformanceResource())
v1_api.register(EventResource())
v1_api.register(PromotionResource())
v1_api.register(StudentResource())
v1_api.register(StudentApplicationResource())
v1_api.register(ArtistResource())
v1_api.register(StaffResource())
v1_api.register(PlaceResource())
v1_api.register(ExhibitionResource())
v1_api.register(ItineraryResource())
v1_api.register(ArtworkResource())

v2_api = routers.DefaultRouter(trailing_slash=False)
v2_api.register(r'people/user', UserViewSet)
v2_api.register(r'people/userprofile', FresnoyProfileViewSet)
v2_api.register(r'people/artist', ArtistViewSet)
v2_api.register(r'people/staff', StaffViewSet)
v2_api.register(r'people/organization', OrganizationViewSet)
v2_api.register(r'school/promotion', PromotionViewSet)
v2_api.register(r'school/student', StudentViewSet)
v2_api.register(r'school/student-application', StudentApplicationViewSet)
v2_api.register(r'school/student/search', StudentAutocompleteSearchViewSet, base_name="school-student-search")
v2_api.register(r'production/film', FilmViewSet)
v2_api.register(r'production/event', EventViewSet)
v2_api.register(r'production/itinerary', ItineraryViewSet)
v2_api.register(r'production/film/genre', FilmGenreViewSet)
v2_api.register(r'production/installation', InstallationViewSet)
v2_api.register(r'production/installation/genre', InstallationGenreViewSet)
v2_api.register(r'production/performance', PerformanceViewSet)
v2_api.register(r'production/collaborator', CollaboratorViewSet)
v2_api.register(r'production/partner', PartnerViewSet)
v2_api.register(r'diffusion/place', PlaceViewSet)
v2_api.register(r'common/beacon', BTBeaconViewSet)
v2_api.register(r'common/website', WebsiteViewSet)
v2_api.register(r'assets/gallery', GalleryViewSet)
v2_api.register(r'assets/medium', MediumViewSet)


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ifresnoy.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^v2/', include(v2_api.urls)),
                       url(r'^v2/auth/', obtain_jwt_token),
                       url(r'^v2/activate/%s/$' % settings.PASSWORD_TOKEN, 'people.views.activate', name='user-activate'),
                       (r'^', include(v1_api.urls)),
                       (r'^grappelli/', include('grappelli.urls')),
                       url('^markdown/', include('django_markdown.urls')),
                       url(r'v1/doc/',
                           include('tastypie_swagger.urls', namespace='ifresnoy_tastypie_swagger'),
                           kwargs={"tastypie_api_module": "ifresnoy.urls.v1_api",
                                   "namespace": "ifresnoy_tastypie_swagger"}),
                       url(r'^admin/', include(admin.site.urls)) \
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
