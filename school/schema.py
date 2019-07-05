import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from school.models import Student, Promotion
from people.schema import UserInput, ArtistInput




class PromoType(DjangoObjectType):
    class Meta:
        model = Promotion
        filter_fields = ['name', 'starting_year', 'ending_year']


class PromoInput(graphene.InputObjectType):
    name = graphene.String()
    starting_year = graphene.String()
    ending_year = graphene.String()


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        filter_fields = ['number', 'promotion__name']

class StudentInput(graphene.InputObjectType):
    user = graphene.List(UserInput)
    promo = graphene.List(PromoInput)
    number = graphene.String()
    artist = graphene.List(ArtistInput)
    graduate = graphene.Boolean()

# class ArtistInput(graphene.InputObjectType):
#     user = graphene.List(UserInput)
#     nickname = graphene.String()
#     bio_short_fr = graphene.String()
#     bio_short_en = graphene.String()
#     bio_fr = graphene.String()
#     bio_en = graphene.String()
#     updated_on = graphene.types.datetime.DateTime
#     twitter_account = graphene.String()
#     facebook_profile = graphene.String()
#
#
# class CreateArtist(graphene.Mutation):
#     class Arguments:
#         input = ArtistInput(required=True)
#
#     ok = graphene.Boolean()
#     artist = graphene.Field(ArtistType)
#
#     @staticmethod
#     def mutate(self, info, input=None):
#         ok = True
#
#         user = User.objects.get(pk=input.user.id)
#         if user is None:
#             return CreateArtist(ok=False, artist=None)
#
#         artist = Artist(
#             user = user,
#             nickname = input.nickname,
#             bio_short_fr = input.bio_short_fr,
#             bio_short_en = input.bio_short_en,
#             bio_fr = input.bio_fr,
#             bio_en = input.bio_en,
#             updated_on = input.updated_on,
#             twitter_account = input.twitter_account,
#             facebook_profile = input.facebook_profile,
#         )
#
#         artist.save()
#
#         return CreateArtist(ok=ok, artist=artist)



class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, id=graphene.Int())
    all_students = graphene.List(StudentType)

    promotion = graphene.Field(PromoType, id=graphene.Int())
    all_promotions = graphene.List(PromoType)


    def resolve_all_students(self, info, **kwargs):
        return Student.objects.all()

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Student.objects.get(pk=id)
        return None

    def resolve_all_promotions(self, info, **kwargs):
        return Promotion.objects.all()

    def resolve_promotion(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Promotion.objects.get(pk=id)
        return None


#
#
# class Mutation(graphene.ObjectType):
#     create_user = CreateUser.Field()
#     update_user = UpdateUser.Field()
#     create_artist = CreateArtist.Field()
