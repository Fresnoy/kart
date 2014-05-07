from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from common.api import WebsiteResource
from assets.api import GalleryResource
from people.api import ArtistResource, StaffResource, OrganizationResource
from diffusion.api import PlaceResource



from .models import Installation, Film, Performance, Event, Itinerary, Artwork

class ProductionResource(ModelResource):
    collaborators = fields.ToManyField(StaffResource, 'collaborators', full=True)
    partners = fields.ToManyField(OrganizationResource, 'partners', full=True)
    websites = fields.ToManyField(WebsiteResource, 'websites', full=True)

class AbstractArtworkResource(ProductionResource):
    """
    A model shared by Artwork subclasses, required to prevent
    dehydrate from looping because of ArtworkResource being shared
    """
    process_galleries = fields.ToManyField(GalleryResource, 'process_galleries', full=True)
    mediation_galleries = fields.ToManyField(GalleryResource, 'mediation_galleries', full=True)
    in_situ_galleries = fields.ToManyField(GalleryResource, 'in_situ_galleries', full=True)
    
    authors = fields.ToManyField(ArtistResource, 'authors')
    
    
class ArtworkResource(AbstractArtworkResource):
    class Meta:
        queryset = Artwork.objects.all()
        resource_name = 'production/artwork'
        filtering = {'authors': ALL_WITH_RELATIONS}

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)

    def dehydrate(self, bundle):
        res_types = (InstallationResource, FilmResource, PerformanceResource)

        for res_type in res_types:
            if isinstance(bundle.obj, res_type.Meta.queryset.model):
                res = res_type()
                rr_bundle = res.build_bundle(obj=bundle.obj, request=bundle.request)
                bundle.data = res.full_dehydrate(rr_bundle).data
                bundle.data['type'] = u"%s" % res_type.Meta.queryset.model.__name__.lower()
                break

        return bundle    

class InstallationResource(AbstractArtworkResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'production/installation'
        filtering = {'authors': ALL_WITH_RELATIONS}                

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)        

class FilmResource(AbstractArtworkResource):
    class Meta:
        queryset = Film.objects.all()
        resource_name = 'production/film'
        filtering = {'authors': ALL_WITH_RELATIONS}        

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)        

class PerformanceResource(AbstractArtworkResource):
    class Meta:
        queryset = Performance.objects.all()
        resource_name = 'production/performance'
        filtering = {'authors': ALL_WITH_RELATIONS}

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)        

class EventResource(ProductionResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'production/event'
    
    place = fields.ForeignKey(PlaceResource, 'place', full=True)

    installations = fields.ToManyField(InstallationResource, 'installations')
    films = fields.ToManyField(FilmResource, 'films')
    performances = fields.ToManyField(PerformanceResource, 'performances')    


class ItineraryResource(ModelResource):
    class Meta:
        queryset = Itinerary.objects.all()
        resource_name = 'production/itinerary'

    artworks = fields.ToManyField(ArtworkResource, 'artworks', full=True)

        
class ExhibitionResource(EventResource):
    class Meta:
        queryset = Event.objects.filter(type='EXHIB')
        resource_name = 'production/exhibition'        

    itineraries = fields.ToManyField(ItineraryResource, 'itineraries', full_list=False, full_detail=True)

