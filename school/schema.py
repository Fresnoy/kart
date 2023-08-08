import graphene
from graphene_django import DjangoObjectType

from datetime import datetime
from people.models import FresnoyProfile
from school.models import Student, Promotion, TeachingArtist, ScienceStudent, PhdStudent, VisitingStudent
from people.schema import ArtistType, ProfileType, DynNameResolver
from people.schema import ArtistEmbeddedInterface
from production.schema import Artwork, ArtworkType


class StudentType(ArtistType):
    class Meta:
        model = Student

    id = graphene.ID(required=True, source='pk')
    artworks = graphene.List(ArtworkType)

    # Retrieve the student's artworks
    def resolve_artworks(self, info):
        return Artwork.objects.filter(authors=self.artist)


class StudentEmbeddedInterface(graphene.Interface):
    '''Interface of models embedding a student field (indirect polymorphism)'''

    # User fields
    firstName = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    lastName = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))

    # FresnoyProfile fields
    photo = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    gender = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    nationality = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    birthdate = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    birthplace = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    birthplace_country = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    homeland_address = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    homeland_zipcode = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    homeland_town = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    homeland_country = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    residence_address = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    residence_zipcode = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    residence_town = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    residence_country = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    homeland_phone = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    residence_phone = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    social_insurance_number = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    family_status = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    mother_tongue = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    other_language = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    cursus = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))

    # Student fields
    number = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    promotion = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    graduate = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    diploma_mention = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))

    def resolve_firstName(self, info):
        return self.student.artist.user.first_name

    def resolve_number(self, info):
        return self.student.number


class TeachingArtistType(DjangoObjectType):
    class Meta:
        model = TeachingArtist
        interfaces = (ArtistEmbeddedInterface,)
    id = graphene.ID(required=True, source='pk')

    # The years during which the TA was active
    years = graphene.List(graphene.String)

    profile = graphene.Field(ProfileType)

    def resolve_profile(self, info):
        return FresnoyProfile.objects.get(user=self.artist.user)

    def resolve_years(self, info):
        # Extract the year of production of each artwork mentored by the TA
        aws = self.artworks_supervision.all()
        # Set to remove duplicates dates
        dates = list(set([aw.production_date.year for aw in aws]))
        return dates


class TeachingArtistsItemType(DjangoObjectType):
    """ Object dedicated to TeachingArtistsList"""
    class Meta:
        model = TeachingArtist

    year = graphene.String()
    teachers = graphene.List(TeachingArtistType)


class ScienceStudentType(DjangoObjectType):
    class Meta:
        model = ScienceStudent
        interfaces = (StudentEmbeddedInterface,)
    id = graphene.ID(required=True, source='pk')


class PhdStudentType(DjangoObjectType):
    class Meta:
        model = PhdStudent
        interfaces = (StudentEmbeddedInterface,)
    id = graphene.ID(required=True, source='pk')


class VisitingStudentType(DjangoObjectType):
    class Meta:
        model = VisitingStudent
        interfaces = (ArtistEmbeddedInterface,)
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
    teachingArtistsList = graphene.List(TeachingArtistsItemType)

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

    def resolve_teachingArtistsList(self, info, **kwargs):
        """ A list of teaching artists grouped by year """
        tal = []
        for ye in range(1997, datetime.now().year):
            tai = TeachingArtistsItemType()
            tai.year = ye
            # Get the TA that mentored artworks for that year
            tai.teachers = set(TeachingArtist.objects.all().filter(
                artworks_supervision__production_date__year=ye))
            tal += [tai]
        return tal

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
