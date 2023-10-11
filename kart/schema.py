import graphene

import people.schema
import school.schema
import production.schema
import assets.schema
import common.schema
import diffusion.schema


class Query(people.schema.Query,
            school.schema.Query,
            production.schema.Query,
            diffusion.schema.Query,
            assets.schema.Query,
            common.schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
