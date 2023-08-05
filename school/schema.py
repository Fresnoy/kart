import graphene
from graphene_django import DjangoObjectType
# from graphql import GraphQLError
# from graphene_django.rest_framework.mutation import SerializerMutation

from school.models import Student, Promotion, TeachingArtist, ScienceStudent, PhdStudent, VisitingStudent
from people.schema import ArtistType
from people.schema import UserEmbeddedInterface, ArtistEmbeddedInterface
from production.schema import Artwork, ArtworkType


class StudentType(ArtistType):
    class Meta:
        model = Student
        filterset_fields = ['number', 'promotion__name']
        interfaces = (UserEmbeddedInterface, ArtistEmbeddedInterface)

    id = graphene.ID(required=True, source='pk')
    artworks = graphene.List(ArtworkType)

    def resolve_artworks(self, info):
        return Artwork.objects.filter(authors=self.artist)


# INTERFACES
# interfaces for objects embedding a user/artist field (indirect polymorphism)
class StudentEmbeddedInterface(graphene.Interface):
    '''Interface of models embedding an artist field (indirect polymorphism)'''
    student = graphene.Field(StudentType)

    def resolve_number(self, info):
        return self.student.number


class TeachingArtistType(DjangoObjectType):
    class Meta:
        model = TeachingArtist
        interfaces = (UserEmbeddedInterface, ArtistEmbeddedInterface)
    id = graphene.ID(required=True, source='pk')


class ScienceStudentType(DjangoObjectType):
    class Meta:
        model = ScienceStudent
        interfaces = (StudentEmbeddedInterface,)
    id = graphene.ID(required=True, source='pk')


class PhdStudentType(DjangoObjectType):
    class Meta:
        model = PhdStudent
    id = graphene.ID(required=True, source='pk')


class VisitingStudentType(DjangoObjectType):
    class Meta:
        model = VisitingStudent
    id = graphene.ID(required=True, source='pk')


class PromoType(DjangoObjectType):
    class Meta:
        model = Promotion
        filterset_fields = ['name', 'starting_year', 'ending_year']

    id = graphene.ID(required=True, source='pk')
    students = graphene.List(StudentType)

    def resolve_students(self, info):
        return Student.objects.filter(promotion=self)
    
    picture = graphene.String()
    # def resolve_picture(self, info):



class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, id=graphene.Int())
    students = graphene.List(StudentType)

    promotion = graphene.Field(PromoType, id=graphene.Int())
    promotions = graphene.List(PromoType)

    teachingArtist = graphene.Field(TeachingArtistType, id=graphene.Int())
    teachingArtists = graphene.List(TeachingArtistType)

    scienceStudent = graphene.Field(ScienceStudentType, id=graphene.Int())
    scienceStudents = graphene.List(ScienceStudentType)

    PhdStudent = graphene.Field(PhdStudentType, id=graphene.Int())
    PhdStudents = graphene.List(PhdStudentType)

    visitingStudent = graphene.Field(VisitingStudentType, id=graphene.Int())
    visitingStudents = graphene.List(VisitingStudentType)

    def resolve_students(self, info, **kwargs):
        return Student.objects.all()

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Student.objects.get(pk=id)
        return None

    def resolve_teachingArtists(self, info, **kwargs):
        return TeachingArtist.objects.all()

    # Teaching artists
    def resolve_teachingArtist(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return TeachingArtist.objects.get(pk=id)
        return None

    # ScienceStudent
    def resolve_scienceStudents(self, info, **kwargs):
        return ScienceStudent.objects.all()

    def resolve_scienceStudent(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return ScienceStudent.objects.get(pk=id)
        return None

    # Phd Students
    def resolve_PhdStudents(self, info, **kwargs):
        return PhdStudent.objects.all()

    def resolve_PhdStudent(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return PhdStudent.objects.get(pk=id)
        return None

    # Visiting Students
    def resolve_visitingStudents(self, info, **kwargs):
        return VisitingStudent.objects.all()

    def resolve_visitingStudent(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return VisitingStudent.objects.get(pk=id)
        return None

    # Promotions
    def resolve_promotions(self, info, **kwargs):
        return Promotion.objects.all()

    def resolve_promotion(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Promotion.objects.get(pk=id)
        return None
