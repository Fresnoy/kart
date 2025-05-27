from django.test import TestCase

import graphene

from kart.schema import Query

from people.tests.factories import ArtistFactory


class TestGQLQueries(TestCase):
    """
    TODO: do tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Following tests about artists queries without filtering
    def test_query_all_artists(self):
        ArtistFactory.create_batch(5)
        # Test the query for all artists
        query = 'query Artists {\
                    artists {\
                        id\
                        displayName\
                        displayPhoto\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        # Check that we have 5 artists in the result
        self.assertEqual(len(result.data['artists']), 5)

    def test_query_filtering_artists(self):
        artists = ArtistFactory.create_batch(5)
        nickname = artists[0].nickname

        # Test the query for all artists
        query = 'query ArtistsSearch($name: String) {\
                    artists(name: $name) {\
                        id\
                        displayName\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={"name": nickname})
        self.assertIsNone(result.errors)
        # Check that we have 1 artists in the result
        self.assertEqual(len(result.data['artists']), 1)
