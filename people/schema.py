import re
import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Artist, FresnoyProfile

from common.schema import WebsiteType

# Types embedding a user field
USER_EMBEDDED_TYPES = ["StudentType", "ArtistType"]
ARTIST_EMBEDDED_TYPES = ["StudentType"]
# User fields
USER_FIELDS = [ff.name for ff in get_user_model()._meta.get_fields()]
# FresnoyProfile fields
FPROFILE_FIELDS = [ff.name for ff in FresnoyProfile._meta.get_fields()]
# print("FPROFILE_FIELDS", FPROFILE_FIELDS)
ARTIST_FIELDS = [ff.name for ff in Artist._meta.get_fields()]

# Camel to snake case
camSnakPat = re.compile(r'(?<!^)(?=[A-Z])')


def cam2snake(cam):
    return camSnakPat.sub('_', cam).lower()


class DynNameResolver:
    def __call__(self, instance, info, **kwargs):

        listReturn = "GraphQLList" in str(type(info.return_type))
        field_name = cam2snake(info.field_name)
        parent_type = str(info.parent_type)
        if parent_type == "UserType":
            if field_name in USER_FIELDS:
                return getattr(instance, field_name)
            if field_name in FPROFILE_FIELDS:
                return getattr(instance.profile, field_name) if instance.profile else None

        if parent_type in USER_EMBEDDED_TYPES:
            if field_name in USER_FIELDS:
                return getattr(instance.user, field_name)
            if field_name in FPROFILE_FIELDS:
                return getattr(instance.user.profile, field_name) if instance.user.profile else None

        if parent_type in ARTIST_EMBEDDED_TYPES:
            if field_name in ARTIST_FIELDS:
                if listReturn:
                    return getattr(instance.artist, field_name).all()
                else:
                    return getattr(instance.artist, field_name)
            if parent_type == "ArtistType":
                if listReturn:
                    return getattr(instance, field_name).all()
                else:
                    return getattr(instance, field_name)


# User
class UserInterface(graphene.Interface):
    id = graphene.ID(required=True)


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
    id = graphene.ID(required=True)
    # bioFr = graphene.String()


class ArtistType(UserType):

    class Meta:
        model = Artist
        interfaces = (graphene.relay.Node, ArtistInterface)

    id = graphene.ID(required=True)
    nickname = graphene.String()
    bioShortFr = graphene.String()
    bioShortEn = graphene.String()
    bioFr = graphene.String()
    bioEn = graphene.String()
    updatedOn = graphene.String()
    twitterAccount = graphene.String()
    facebookProfile = graphene.String()
    websites = graphene.List(WebsiteType)

    resolve_id = DynNameResolver()
    resolve_nickname = DynNameResolver()
    resolve_bioShortFr = DynNameResolver()
    resolve_bioShortEn = DynNameResolver()
    resolve_bioFr = DynNameResolver()
    resolve_bioEn = DynNameResolver()
    resolve_updatedOn = DynNameResolver()
    resolve_twitterAccount = DynNameResolver()
    resolve_facebookProfile = DynNameResolver()
    resolve_websites = DynNameResolver()

    # def resolve_websites(self, info, **kwargs):
    #     return self.websites.all() if self.websites else None


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
