# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie import fields

from .models import Place, Award, MetaAward


class PlaceResource(ModelResource):
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'diffusion/place'


class AwardResource(ModelResource):
    class Meta:
        queryset = Award.objects.all()
        resource_name = 'diffusion/award'

    meta_award = fields.ForeignKey('diffusion.api.MetaAwardResource',
                                   'meta_award',
                                   full=True,
                                   blank=True,
                                   null=True)

    artwork = fields.ToManyField('production.api.ArtworkResource', 'artwork',
                                 full=True, blank=True, null=True)
    artist = fields.ToManyField('people.api.UserResource', 'artist', full=True, null=True)
    event = fields.ForeignKey('production.api.EventResource', 'event', null=True, )
    giver = fields.ToManyField('people.api.UserResource', 'giver', full=True, null=True)
    sponsor = fields.ForeignKey('people.api.OrganizationResource', 'sponsor', full=True, null=True, )


class MetaAwardResource(ModelResource):
    class Meta:
        queryset = MetaAward.objects.all()
        resource_name = 'diffusion/meta-award'

    event = fields.ForeignKey('production.api.EventResource', 'event', full=True)
    task = fields.ForeignKey('production.api.StaffTaskResource', 'task', full=True, null=True)
