import re
import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Artist, FresnoyProfile, Staff
from school.models import Student

from common.schema import WebsiteType

# User fields
USER_FIELDS = [ff.name for ff in get_user_model()._meta.get_fields()]
# FresnoyProfile fields
FPROFILE_FIELDS = [ff.name for ff in FresnoyProfile._meta.get_fields()]
# Artist Fields
ARTIST_FIELDS = [ff.name for ff in Artist._meta.get_fields()]
# Student fields
STUDENT_FIELDS = [ff.name for ff in Student._meta.get_fields()]


def camel2snake(cam):
    # Camel to snake case
    camSnakPat = re.compile(r'(?<!^)(?=[A-Z])')
    return camSnakPat.sub('_', cam).lower()


class DynNameResolver:

    def __init__(self, interface=""):
        self.interface = interface

    def __call__(self, instance, info, **kwargs):

        # For GraphQLList, a list is expected to be returned
        listReturn = "GraphQLList" in str(type(info.return_type))
        # Back convert camelCase to sn_ake to match django's syntax
        field_name = camel2snake(info.field_name)
        # The type of the targeted object
        parent_type = str(info.parent_type)

        user = artist = profile = student = obj = None

        if self.interface == "ProfileEmbedded":
            profile = self.profile

        if self.interface == "StudentEmbedded":
            user = instance.student.user
            artist = instance.student.artist
            student = instance

        if self.interface == "ArtistEmbedded":
            user = instance.artist.user
            artist = instance.artist

        if self.interface == "UserEmbedded":
            user = instance.user

        if parent_type == "ArtistType":
            user = instance.user
            artist = instance

        if parent_type == "StudentType":
            student = instance
            user = instance.user

        if parent_type == "UserType":
            user = instance

        try:
            profile = FresnoyProfile.objects.get(user=user)
        except Exception:
            profile = None

        if field_name in STUDENT_FIELDS:
            obj = student
        elif field_name in ARTIST_FIELDS:
            obj = artist
        elif field_name in USER_FIELDS:
            obj = user
        elif field_name in FPROFILE_FIELDS:
            obj = profile
        else:
            print("fieldname not found", field_name)

        # print("parent_type", parent_type, "OBJ", type(obj), "FIELD NAME",
        #       field_name, "interface", self.interface)

        if hasattr(obj, field_name):
            if listReturn:
                return getattr(obj, field_name).all()
            else:
                return getattr(obj, field_name)
        else:
            return None

# INTERFACES
# interfaces for objects embedding a user/artist field (indirect polymorphism)


class UserEmbeddedInterface(graphene.Interface):
    '''Interface of models embedding a user field (indirect polymorphism)'''
    firstName = graphene.String(resolver=DynNameResolver())
    lastName = graphene.String()
    photo = graphene.String()


class ArtistEmbeddedInterface(graphene.Interface):
    '''Interface of models embedding an artist field (indirect polymorphism)'''

    # User fields
    firstName = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    lastName = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))

    # FresnoyProfile fields
    photo = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    gender = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    nationality = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    birthdate = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    birthplace = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    birthplace_country = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    homeland_address = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    homeland_zipcode = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    homeland_town = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    homeland_country = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    residence_address = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    residence_zipcode = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    residence_town = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    residence_country = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    homeland_phone = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    residence_phone = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    social_insurance_number = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    family_status = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    mother_tongue = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    other_language = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    cursus = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))

    # Artist fields
    nickname = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    bioShortFr = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    bioShortEn = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    bioFr = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    bioEn = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    updatedOn = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    twitterAccount = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    facebookProfile = graphene.String(
        resolver=DynNameResolver(interface="ArtistEmbedded"))
    websites = graphene.List(WebsiteType)


class ProfileEmbeddedInterface(graphene.Interface):
    '''Interface of models embedding an artist field (indirect polymorphism)'''
    gender = graphene.String()
    nationality = graphene.String()
    birthdate = graphene.String()
    birthplace = graphene.String()
    birthplace_country = graphene.String()
    homeland_address = graphene.String()
    homeland_zipcode = graphene.String()
    homeland_town = graphene.String()
    homeland_country = graphene.String()
    residence_address = graphene.String()
    residence_zipcode = graphene.String()
    residence_town = graphene.String()
    residence_country = graphene.String()
    homeland_phone = graphene.String()
    residence_phone = graphene.String()
    social_insurance_number = graphene.String()
    family_status = graphene.String()
    mother_tongue = graphene.String()
    other_language = graphene.String()
    cursus = graphene.String()

# User


class UserInterface(graphene.Interface):
    id = graphene.ID(required=True, source='pk')


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (UserInterface,)

    firstName = graphene.String(resolver=DynNameResolver())
    lastName = graphene.String(resolver=DynNameResolver())
    photo = graphene.String(resolver=DynNameResolver())
    gender = graphene.String(resolver=DynNameResolver())
    nationality = graphene.String(resolver=DynNameResolver())
    birthdate = graphene.String(resolver=DynNameResolver())
    birthplace = graphene.String(resolver=DynNameResolver())
    birthplaceCountry = graphene.String(resolver=DynNameResolver())
    homelandAddress = graphene.String(resolver=DynNameResolver())
    homelandZipcode = graphene.String(resolver=DynNameResolver())
    homelandTown = graphene.String(resolver=DynNameResolver())
    homelandCountry = graphene.String(resolver=DynNameResolver())
    residenceAddress = graphene.String(resolver=DynNameResolver())
    residenceZipcode = graphene.String(resolver=DynNameResolver())
    residenceTown = graphene.String(resolver=DynNameResolver())
    residenceCountry = graphene.String(resolver=DynNameResolver())
    homelandPhone = graphene.String(resolver=DynNameResolver())
    residencePhone = graphene.String(resolver=DynNameResolver())
    socialInsuranceNumber = graphene.String(resolver=DynNameResolver())
    familyStatus = graphene.String(resolver=DynNameResolver())
    motherTongue = graphene.String(resolver=DynNameResolver())
    otherLanguage = graphene.String(resolver=DynNameResolver())
    cursus = graphene.String(resolver=DynNameResolver())


# FresnoProfile
class FresnoyProfileInterface(graphene.Interface):
    user = graphene.Field(UserType, id=graphene.Int())


class FresnoyProfileType(DjangoObjectType):
    class Meta:
        model = FresnoyProfile

# Artist


class ArtistInterface(graphene.Interface):
    id = graphene.ID(required=True, source='pk')


class ArtistType(UserType):

    class Meta:
        model = Artist
        interfaces = (graphene.relay.Node, ArtistInterface)

    id = graphene.ID(required=True, source='pk')

    nickname = graphene.String(resolver=DynNameResolver())
    bioShortFr = graphene.String(resolver=DynNameResolver())
    bioShortEn = graphene.String(resolver=DynNameResolver())
    bioFr = graphene.String(resolver=DynNameResolver())
    bioEn = graphene.String(resolver=DynNameResolver())
    updatedOn = graphene.String(resolver=DynNameResolver())
    twitterAccount = graphene.String(resolver=DynNameResolver())
    facebookProfile = graphene.String(resolver=DynNameResolver())
    websites = graphene.List(WebsiteType, resolver=DynNameResolver())


class StaffType(UserType):
    class Meta:
        model = Staff


class ProfileType(DjangoObjectType):
    class Meta:
        model = FresnoyProfile


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    artist = graphene.Field(ArtistType, id=graphene.Int())
    artists = graphene.List(ArtistType)

    profile = graphene.Field(FresnoyProfileType, id=graphene.Int())
    profiles = graphene.List(FresnoyProfileType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(pk=id)
        return None

    def resolve_artists(self, info, **kwargs):
        return Artist.objects.all()

    def resolve_artist(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Artist.objects.get(pk=id)
        return None

    def resolve_profiles(self, info, **kwargs):
        return FresnoyProfile.objects.all()

    def resolve_profile(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return FresnoyProfile.objects.get(pk=id)
        return None
