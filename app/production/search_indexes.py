from haystack import indexes
from .models import Film, Performance, Installation


class FilmIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    keywords = indexes.MultiValueField(model_attr='keywords', null=True)
    genres = indexes.MultiValueField(null=True,)
    shooting_place = indexes.MultiValueField(null=True,)
    type = indexes.CharField(null=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def prepare_type(self, obj):
        return "Film"

    def prepare_keywords(self, obj):
        if obj.keywords.all().count():
            keywords = [keyword.name for keyword in obj.keywords.all()]
            return keywords
        return ""

    def prepare_shooting_place(self, obj):
        if obj.shooting_place.all().count():
            places = [place.address for place in obj.shooting_place.all()]
            return places
        return ""

    def prepare_genres(self, obj):
        if obj.genres.all().count():
            genres = [genre.label for genre in obj.genres.all()]
            return genres
        return ""

    def get_model(self):
        return Film

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()


class InstallationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    genres = indexes.MultiValueField(null=True,)
    content_auto = indexes.EdgeNgramField(model_attr='title')
    type = indexes.CharField(null=True)

    def prepare_type(self, obj):
        return "Installation"

    def prepare_genres(self, obj):
        if obj.genres.all().count():
            genres = [genre.label for genre in obj.genres.all()]
            return genres
        return ""

    def get_model(self):
        return Installation

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()


class PerformanceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')
    type = indexes.CharField(null=True)

    def prepare_type(self, obj):
        return "Performance"

    def get_model(self):
        return Performance

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()
