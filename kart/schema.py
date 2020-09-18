import graphene

import people.schema
import school.schema


class Query(people.schema.Query, school.schema.Query, graphene.ObjectType):
    pass


class Mutation(people.schema.Mutation, school.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
