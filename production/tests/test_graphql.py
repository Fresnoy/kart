from django.test import TestCase

import graphene

from kart.schema import Query
from production.tests.factories import EventFactory, PerformanceFactory
from people.tests.factories import ArtistFactory


class TestGQLPages(TestCase):
    """
    TODO: do tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_query_artworkx_panox(self):
        # create
        self.event = EventFactory()
        self.artist = ArtistFactory()
        self.performance = PerformanceFactory(authors=[self.artist])
        self.event.performances.add(self.performance)
        self.event.save()

        query = "query ArtworkXPanoX($expo: Int, $oeuvre: ID) {\
                    exhibition(id: $expo) {\
                        title\
                        artworkExhib(id: $oeuvre) {\
                            artwork {\
                                id\
                                title\
                                picture\
                                type\
                                descriptionFr\
                                descriptionEn\
                                thanksFr\
                                thanksEn\
                                productionDate\
                                inSituGalleries {\
                                    media {\
                                        picture }\
                                }\
                                authors {\
                                    id\
                                    displayName\
                                    firstName\
                                    lastName\
                                    bioFr\
                                    bioEn }\
                                partners {\
                                    name}\
                            }\
                            prevAlpha {\
                                id }\
                            nextAlpha {\
                                id}\
                        }\
                    }\
                }"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'expo': self.event.id, 'oeuvre': self.performance.id})
        self.assertIsNone(result.errors)

    def test_query_exhibx(self):
        event = EventFactory()
        artist = ArtistFactory()
        performance = PerformanceFactory(authors=[artist])
        event.performances.add(performance)
        event.save()

        query = 'query exhib($idExhib: Int) {\
                    exhibition(id: $idExhib) {\
                        artworks {\
                            id\
                            authors {\
                            id\
                            displayName\
                            }\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'idExhib': event.id, })
        self.assertIsNone(result.errors)
