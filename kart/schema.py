import graphene

import people.schema
import school.schema
import production.schema


class Query(people.schema.Query,
            school.schema.Query,
            production.schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
