from haystack import indexes
from .models import Student


class StudentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    firstname = indexes.CharField(model_attr="user__first_name")
    lastname = indexes.CharField(model_attr="user__last_name")
    promotion = indexes.CharField(model_attr="promotion")
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Student

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()
