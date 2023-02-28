from haystack import indexes
from .models import Artist


class ArtistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    firstname = indexes.CharField(model_attr='user__first_name')
    lastname = indexes.CharField(model_attr='user__last_name')
    nationality = indexes.MultiValueField(null=True,)
    content_auto = indexes.EdgeNgramField(use_template=True)

    def prepare_nationality(self, obj):
        try:
            nationality = obj.user.profile.nationality
            return nationality.split(",")
        except Exception:
            return None

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        Artists are with an arwork or is student
        """
        from django.db.models import Q
        return self.get_model().objects.filter(Q(artworks__isnull=False) | Q(student__isnull=False)).distinct()
