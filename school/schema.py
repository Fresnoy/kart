import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required

from datetime import datetime

# from diffusion.models import Diffusion
from people.models import FresnoyProfile
from school.models import (Student, Promotion, TeachingArtist, ScienceStudent, PhdStudent, VisitingStudent,
                           StudentApplication, StudentApplicationSetup, AdminStudentApplication)
from people.schema import ProfileType, DynNameResolver, ArtistEmbeddedInterface
from production.schema import Artwork, ArtworkType
from diffusion.schema import DiffusionType
from assets.schema import GalleryType


def order(students, orderby):
    # Sort the students

    def tt(x):
        if orderby == "displayName":
            if x.artist.alphabetical_order != "":
                art = x.artist.alphabetical_order
            elif x.artist.nickname != "":
                art = x.artist.nickname
            else:
                art = x.artist.user.last_name
        else:
            raise Exception("orderby value is undefined or unknown")
        return (art)

    return sorted(students, key=lambda x: tt(x))


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        interfaces = (ArtistEmbeddedInterface,)

    id = graphene.ID(required=True, source='pk')
    artworks = graphene.List(ArtworkType)

    # Retrieve the student's artworks
    def resolve_artworks(parent, info):
        return Artwork.objects.filter(authors=parent.artist)


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

    # Artist fields
    displayName = graphene.String()

    # Student fields
    number = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    promotion = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    graduate = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    diploma_mention = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))

    def resolve_displayName(parent, info):
        if parent.student.artist.nickname:
            return parent.student.artist.nickname
        else:
            return f"{parent.student.user.first_name} {parent.student.user.last_name}"

    def resolve_number(parent, info):
        return parent.student.number


class TeachingArtistType(DjangoObjectType):
    class Meta:
        model = TeachingArtist
        interfaces = (ArtistEmbeddedInterface,)

    id = graphene.ID(required=True, source='pk')

    diffusions = graphene.List(DiffusionType)

    # The years during which the TA was active
    years = graphene.List(graphene.String)

    pictures_gallery = graphene.Field(GalleryType)

    profile = graphene.Field(ProfileType)

    def resolve_profile(parent, info):
        return FresnoyProfile.objects.get(user=parent.artist.user)

    def resolve_years(parent, info):
        # Extract the year of production of each artwork mentored by the TA
        aws = parent.artworks_supervision.all()
        # Set to remove duplicates dates
        dates = list(set([aw.production_date.year for aw in aws]))
        return dates


class TeachingArtistsItemType(DjangoObjectType):
    """ Object dedicated to TeachingArtistsList"""
    class Meta:
        model = TeachingArtist

    years = graphene.List(graphene.Int)
    teachers = graphene.List(TeachingArtistType)

    def resolve_years(parent, info):
        # Extract the year of production of each artwork mentored by the TA
        aws = parent.artworks_supervision.all()
        # Set to remove duplicates dates
        dates = list(set([aw.production_date.year for aw in aws]))
        return dates

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

    def resolve_students(parent, info):
        students = Student.objects.filter(promotion=parent)
        return order(students, "displayName")

    picture = graphene.String()
    # def resolve_picture(parent, info):


class StudentApplicationSetupType(DjangoObjectType):
    class Meta:
        model = StudentApplicationSetup

    id = graphene.ID(required=True, source='pk')

    def resolve_selected_publish_date(self, info):
        return self.selected_publish_date.astimezone() if self.selected_publish_date else None

    def resolve_interviews_publish_date(self, info):
        return self.interviews_publish_date.astimezone() if self.interviews_publish_date else None

    def resolve_candidature_date_start(self, info):
        return self.candidature_date_start.astimezone() if self.candidature_date_start else None

    def resolve_candidature_date_end(self, info):
        return self.candidature_date_end.astimezone() if self.candidature_date_end else None

    def resolve_information_and_tour_date(self, info):
        return self.information_and_tour_date.astimezone() if self.information_and_tour_date else None


class StudentApplicationType(DjangoObjectType):
    class Meta:
        model = StudentApplication
        filterset_fields = ("campaign__is_current_setup",)
        # interfaces = (ArtistEmbeddedInterface,)

    id = graphene.ID(required=True, source='pk')


class StudentApplicationAdminInterface(graphene.Interface):
    id = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))
    selected = graphene.String(
        resolver=DynNameResolver(interface="StudentEmbedded"))


class StudentApplicationAdminType(DjangoObjectType):
    class Meta:
        model = AdminStudentApplication
        interfaces = (graphene.relay.Node,)
        fields = "__all__"
        filter_fields = ('application__application_completed',
                         'application_complete',
                         'selected_for_interview', 'application__remote_interview',
                         'wait_listed_for_interview', 'selected', 'unselected',
                         'application__campaign__is_current_setup',
                         'wait_listed',)

    id = graphene.ID(required=True, source='pk')

    def resolve_interview_date(self, info):
        # why not giving tz ?
        return self.interview_date.astimezone() if self.interview_date else None


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

    studentApplication = graphene.Field(StudentApplicationType, id=graphene.Int())
    studentApplications = graphene.List(StudentApplicationType)

    # Setup can be filtered by id or by current_setup
    studentApplicationSetup = graphene.Field(StudentApplicationSetupType, id=graphene.Int(),
                                             is_current_setup=graphene.Boolean(required=False))
    studentApplicationSetups = graphene.List(StudentApplicationSetupType)

    studentApplicationAdmin = graphene.Field(StudentApplicationAdminType, id=graphene.Int())
    studentApplicationAdmins = DjangoFilterConnectionField(StudentApplicationAdminType, max_limit=None)

    def resolve_students(root, info, **kwargs):
        students = Student.objects.all()
        # order by displayName by default
        return order(students, "displayName")

    def resolve_student(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Student.objects.get(pk=id)
        return None

    def resolve_teachingArtists(root, info, **kwargs):
        return TeachingArtist.objects.all()

    def resolve_teachingArtistsList(root, info, **kwargs):
        """ A list of teaching artists grouped by year """
        tal = []
        for ye in range(1997, datetime.now().year + 2):
            tai = TeachingArtistsItemType()
            tai.year = ye
            # Get the TA that mentored artworks for that year
            tai.teachers = set(TeachingArtist.objects.all().filter(
                artworks_supervision__production_date__year=ye))
            tai.teachers = order(tai.teachers, "displayName")
            tal += [tai]
        return tal

    # Teaching artists
    def resolve_teachingArtist(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return TeachingArtist.objects.get(pk=id)
        return None

    # ScienceStudent
    def resolve_scienceStudents(root, info, **kwargs):
        return ScienceStudent.objects.all()

    def resolve_scienceStudent(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return ScienceStudent.objects.get(pk=id)
        return None

    # Phd Students
    def resolve_PhdStudents(root, info, **kwargs):
        return PhdStudent.objects.all()

    def resolve_PhdStudent(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return PhdStudent.objects.get(pk=id)
        return None

    # Visiting Students
    def resolve_visitingStudents(root, info, **kwargs):
        return VisitingStudent.objects.all()

    def resolve_visitingStudent(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return VisitingStudent.objects.get(pk=id)
        return None

    # Promotions
    def resolve_promotions(root, info, **kwargs):
        return Promotion.objects.all()

    def resolve_promotion(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Promotion.objects.get(pk=id)
        return None

    # student applications
    def resolve_studentApplications(root, info, **kwargs):
        # only staff
        if info.context.user.is_staff:
            return StudentApplication.objects.all()
        return None

    def resolve_studentApplication(root, info, **kwargs):
        # get id
        id = kwargs.get('id')
        if id is not None and info.context.user.is_staff:
            return StudentApplication.objects.get(pk=id)
        return None

    def resolve_studentApplicationSetup(root, info, **kwargs):
        # get id
        id = kwargs.get('id')
        # get current (is_current_setup)
        is_current_setup = kwargs.get('is_current_setup')
        if info.context.user.is_authenticated:
            if id:
                return StudentApplicationSetup.objects.get(pk=id)
            if is_current_setup is not None:
                return StudentApplicationSetup.objects.filter(is_current_setup=is_current_setup).first()
        return None

    def resolve_studentApplicationSetups(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return StudentApplicationSetup.objects.all()
        return None

    @staff_member_required
    def resolve_studentApplicationAdmins(root, info, **kwargs):
        return AdminStudentApplication.objects.all()

    @staff_member_required
    def resolve_studentApplicationAdmin(root, info, **kwargs):
        return AdminStudentApplication.objects.get(pk=id)
