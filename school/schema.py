import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene_django.rest_framework.mutation import SerializerMutation

from school.models import Student, Promotion, Artist
from people.schema import UserInput, ArtistInput






class PromoType(DjangoObjectType):
    class Meta:
        model = Promotion
        filter_fields = ['name', 'starting_year', 'ending_year']


class PromoInput(graphene.InputObjectType):
    id = graphene.String()
    name = graphene.String()
    starting_year = graphene.String()
    ending_year = graphene.String()


class CreatePromo(graphene.Mutation):
    class Arguments:
        input = PromoInput(required=True)

    ok = graphene.Boolean()
    promo = graphene.Field(PromoType)

    @staticmethod
    def mutate(self, info, input=None):
        promo = Promotion(
            name = input.name,
            starting_year = input.starting_year,
            ending_year = input.ending_year,
        )
        ok = True
        promo.save()
        return CreatePromo(promo=promo, ok=ok)


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        filter_fields = ['number', 'promotion__name']

class StudentInput(graphene.InputObjectType):
    id = graphene.String()
    user = graphene.Field(UserInput)
    promotion = graphene.Field(PromoInput)
    number = graphene.String()
    artist = graphene.Field(ArtistInput)
    graduate = graphene.Boolean()


class CreateStudent(graphene.Mutation):
    class Arguments:
        input = StudentInput(required=True)

    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(self, info, input=None):
        print("ARTIST", input.artist.id)

        try:
            artist = Artist.objects.get(pk=input.artist.id)
        except :
            return CreateStudent(ok=False, student=None)

        # The Student model requires an Artist AND a user
        # This looks at least surprising
        # TODO : delete user from Artist

        try :
            promotion = Promotion.objects.get(pk=input.promotion.id)
        except :
            return CreateStudent(ok=False, student=None)

        print("promo", promotion)

        student = Student(
            user = artist.user,
            promotion = promotion,
            number = input.number,
            artist = artist,
            graduate = input.graduate,
        )
        ok = True
        student.save()
        return CreateStudent(student=student, ok=ok)


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




class Mutation(graphene.ObjectType):
    create_promo = CreatePromo.Field()
    create_student = CreateStudent.Field()
