from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from people.api import ArtistResource, StaffResource, OrganizationResource
from production.api import (
    InstallationResource, FilmResource,
    PerformanceResource, EventResource, ExhibitionResource,
    ItineraryResource, ArtworkResource, StaffTaskResource
)
from diffusion.api import PlaceResource
from school.api import PromotionResource, StudentResource, StudentApplicationResource

from people.views import (
    ArtistViewSet, UserViewSet, FresnoyProfileViewSet,
    StaffViewSet, OrganizationViewSet
)
from school.views import (
    PromotionViewSet, StudentViewSet,
    StudentAutocompleteSearchViewSet, StudentApplicationViewSet, StudentApplicationSetupViewSet
)
from production.views import (
    ArtworkViewSet, FilmViewSet, InstallationViewSet,
    PerformanceViewSet, FilmGenreViewSet,
    InstallationGenreViewSet, EventViewSet,
    ItineraryViewSet,
    CollaboratorViewSet, PartnerViewSet, OrganizationTaskViewSet
)
from diffusion.views import PlaceViewSet, AwardViewSet, MetaAwardViewSet
from common.views import BTBeaconViewSet, WebsiteViewSet
from assets.views import GalleryViewSet, MediumViewSet


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(InstallationResource())
v1_api.register(FilmResource())
v1_api.register(PerformanceResource())
v1_api.register(EventResource())
v1_api.register(OrganizationResource())
v1_api.register(StaffTaskResource())
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
v2_api.register(r'people/organization-staff', OrganizationTaskViewSet)
v2_api.register(r'school/promotion', PromotionViewSet)
v2_api.register(r'school/student', StudentViewSet)
v2_api.register(r'school/student-application', StudentApplicationViewSet)
v2_api.register(r'school/student-application-setup', StudentApplicationSetupViewSet)
v2_api.register(r'school/student/search', StudentAutocompleteSearchViewSet, base_name="school-student-search")
v2_api.register(r'production/artwork', ArtworkViewSet)
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
v2_api.register(r'diffusion/meta-award', MetaAwardViewSet)
v2_api.register(r'diffusion/award', AwardViewSet)
v2_api.register(r'common/beacon', BTBeaconViewSet)
v2_api.register(r'common/website', WebsiteViewSet)
v2_api.register(r'assets/gallery', GalleryViewSet)
v2_api.register(r'assets/medium', MediumViewSet)


urlpatterns = patterns('',
                       url(r'^v2/', include(v2_api.urls)),
                       url(r'^v2/auth/', obtain_jwt_token),
                       url(r'^account/activate/%s/$' % settings.PASSWORD_TOKEN,
                           'people.views.activate', name='user-activate'),
                       # django user registration
                       url(r'^v2/rest-auth/', include('rest_auth.urls')),
                       url(r'^v2/rest-auth/registration/', include('rest_auth.registration.urls')),
                       # vimeo
                       url(r'^v2/assets/vimeo/upload/token',
                           'assets.views.vimeo_get_upload_token', name='vimeo-upload-token'),
                       # send emails
                       url(r'^v2/people/send-emails',
                           'people.views.send_custom_emails', name='send-emails'),

                       # api v1
                       (r'^', include(v1_api.urls)),
                       (r'^grappelli/', include('grappelli.urls')),
                       url('^markdown/', include('django_markdown.urls')),
                       url(r'v1/doc/',
                           include('tastypie_swagger.urls', namespace='kart_tastypie_swagger'),
                           kwargs={"tastypie_api_module": "kart.urls.v1_api",
                                   "namespace": "kart_tastypie_swagger"}),
                       url(r'^static/(?P<path>.*)$',
                           'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT}),
                       url(r'^admin/', include(admin.site.urls)) \
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
