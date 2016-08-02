from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer


from .models import Promotion, Student
from .search_indexes import StudentIndex


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion


class StudentAutocompleteSerializer(HaystackSerializer):
    class Meta:
        index_classes = [StudentIndex]
        fields = ["firstname", "lastname"]
        ignore_fields = ["autocomplete"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "autocomplete"
        }

