from django.db import models

from people.models import Artist
from assets.models import Gallery

class Production(models.Model):
    class Meta:
        abstract = True
        
    production_date = models.DateField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    picture = models.ImageField(upload_to='production/')    

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.title
    
    
class Artwork(Production):
    credits_fr = models.TextField(blank=True, null=True)
    credits_en = models.TextField(blank=True, null=True)

    thanks_fr = models.TextField(blank=True, null=True)
    thanks_en = models.TextField(blank=True, null=True)

    copyright_fr = models.TextField(blank=True, null=True)
    copyright_en = models.TextField(blank=True, null=True)
    
    process_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_process')
    mediation_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_mediation')
    in_situ_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_insitu')

    authors = models.ManyToManyField(Artist, related_name="%(class)s")    
    
    
class Film(Artwork):
    pass

class Installation(Artwork):
    technical_description = models.TextField(blank=True)

class Performance(Artwork):
    pass

class Task(models.Model):
    pass