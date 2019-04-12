import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model

from .models import Artist


########################## User


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    # first_name = graphene.String()
    # last_name = graphene.String()

class CreateUser(graphene.Mutation):

    user = graphene.Field(UserType)
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(ok=True, user=user)


########################## Artist

class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist

    # Retrieve the usual name from the model's method
    usual_name = graphene.String()
    def resolve_usual_name(self, info, **kwargs):
        return self.get_displayName()


class ArtistInput(graphene.InputObjectType):
    user = graphene.List(UserInput)
    nickname = graphene.String()
    bio_short_fr = graphene.String()
    bio_short_en = graphene.String()
    bio_fr = graphene.String()
    bio_en = graphene.String()
    updated_on = graphene.types.datetime.DateTime
    twitter_account = graphene.String()
    facebook_profile = graphene.String()



class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    artists = graphene.List(ArtistType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_artists(self, info, **kwargs):
        return Artist.objects.all()


class CreateArtist(graphene.Mutation):
    class Arguments:
        input = ArtistInput(required=True)

    ok = graphene.Boolean()
    artist = graphene.Field(ArtistType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = True

        user = User.objects.get(pk=input.user.id)
        if user is None:
            return CreateArtist(ok=False, artist=None)

        artist = Artist(
            user = user,
            nickname = input.nickname,
            bio_short_fr = input.bio_short_fr,
            bio_short_en = input.bio_short_en,
            bio_fr = input.bio_fr,
            bio_en = input.bio_en,
            updated_on = input.updated_on,
            twitter_account = input.twitter_account,
            facebook_profile = input.facebook_profile,
        )

        artist.save()

        return CreateArtist(ok=ok, artist=artist)

class Mutation(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    create_user = CreateUser.Field()
