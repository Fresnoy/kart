import graphene

import people.schema

class Query(people.schema.Query, graphene.ObjectType):
    pass

class Mutation(people.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
