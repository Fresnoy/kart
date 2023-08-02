import graphene
from graphene_django import DjangoObjectType
# from graphql import GraphQLError
# from graphene_django.rest_framework.mutation import SerializerMutation

from school.models import Student, Promotion
from people.schema import ArtistType
from production.schema import Artwork, ArtworkType


class StudentType(ArtistType):
    class Meta:
        model = Student
        filterset_fields = ['number', 'promotion__name']

    artworks = graphene.List(ArtworkType)

    def resolve_artworks(self, info):
        return Artwork.objects.filter(authors=self.artist)


class PromoType(DjangoObjectType):
    class Meta:
        model = Promotion
        filterset_fields = ['name', 'starting_year', 'ending_year']

    students = graphene.List(StudentType)

    def resolve_students(self, info):
        return Student.objects.filter(promotion=self)


class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, id=graphene.Int())
    students = graphene.List(StudentType)

    promotion = graphene.Field(PromoType, id=graphene.Int())
    promotions = graphene.List(PromoType)

    def resolve_students(self, info, **kwargs):
        return Student.objects.all()

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Student.objects.get(pk=id)
        return None

    def resolve_promotions(self, info, **kwargs):
        return Promotion.objects.all()

    def resolve_promotion(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Promotion.objects.get(pk=id)
        return None
