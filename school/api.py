from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from .models import Promotion, Student

class PromotionResource(ModelResource):
    class Meta:
        queryset = Promotion.objects.all()
        resource_name = 'school/promotion'

class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'school/student'
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'promotion': ALL,
        }


    promotion = fields.ForeignKey(PromotionResource, 'promotion')
