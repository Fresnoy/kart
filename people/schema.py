import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Artist


########################## User


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = False
        # Username validation
        if ' ' in input.username:
            raise GraphQLError('No space allowed in username')
        # Check if username not already taken
        if not User.objects.filter(username=input.username).exists():
            user_instance = User.objects.create_user(username=input.username, email=input.email, password=input.password)
            ok = True
            return CreateUser(ok=True, user=user_instance)
        raise GraphQLError('Username already exists.')



class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = get_user_model()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        print(">>>>>>>>>>>>>>>>>>>>>>>> id : ",id)
        if user_instance:
            ok = True
            user_instance.usernamne = input.username
            user_instance.email = input.email
            user_instance.set_password(input.password)
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


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



class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)
    artist = graphene.Field(ArtistType, id=graphene.Int())
    artists = graphene.List(ArtistType)

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




class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_artist = CreateArtist.Field()
