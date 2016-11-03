from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage

from haystack.query import SearchQuerySet
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash

from people.api import ArtistResource, UserResource
from .models import Promotion, Student, StudentApplication

class PromotionResource(ModelResource):
    class Meta:
        queryset = Promotion.objects.all()
        resource_name = 'school/promotion'
        ordering = ['starting_year']


class StudentApplicationResource(ModelResource):
    class Meta:
        queryset = StudentApplication.objects.all()
        resource_name = 'school/application'

    artist = fields.ForeignKey(ArtistResource, 'artist')


class StudentResource(ArtistResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'school/student'
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'promotion': ALL,
        }

    promotion = fields.ForeignKey(PromotionResource, 'promotion')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Student).load_all().autocomplete(content_auto=request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
