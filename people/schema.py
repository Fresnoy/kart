import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Artist, FresnoyProfile


# User


class UserInterface(graphene.Interface):
    id = graphene.ID(required=True)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (UserInterface,)


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
    firstName = graphene.String()
    lastName = graphene.String()
    nationality = graphene.String()

    def resolve_firstName(self, info):
        return self.user.first_name

    def resolve_lastName(self, info):
        return self.user.last_name

    def resolve_nationality(self, info):
        return self.user.profile.nationality if self.user.profile else None


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
