from django.db import models

from people.models import Organization


class Place(models.Model):
    """
    Some place belonging to an organization
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    organization = models.ForeignKey(Organization, related_name='places')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.organization)


class Award(models.Model):
    """
    Awards given to artworks & such.
    """
    pass
    # event
    # artwork
    # -> award (textfield)
