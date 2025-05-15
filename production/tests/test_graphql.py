from django.test import TestCase

import graphene

from kart.schema import Query
from production.tests.factories import (
    EventFactory,
    PerformanceFactory,
    ArtworkFactory,
    KeywordFactory
)
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

    def test_query_all_artworks_keywords(self):
        query = 'query ArtworksKeywords {\
                    artworks {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    def test_query_all_productions_artworks_keywords(self):
        query = 'query AllProductionsArtworksKeywords {\
                    productions {\
                        ... on ArtworkType {\
                            keywords {\
                                name\
                            }\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    def test_query_specific_artwork_keywords(self):
        artwork = ArtworkFactory()
        keyword = KeywordFactory()
        artwork.keywords.add(keyword)
        artwork.save()

        query = 'query ArtworkKeywords($artworkId: Int) {\
                    artwork(id: $artworkId) {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'artworkId': artwork.id})
        self.assertIsNone(result.errors)

    def test_query_specific_artwork_keywords_with_two_keywords(self):
        artwork = ArtworkFactory()
        firstKeyword = KeywordFactory(name='mythe')
        secondKeyword = KeywordFactory(name='société')
        artwork.keywords.add(firstKeyword, secondKeyword)
        artwork.save()

        query = 'query ArtworkKeywords($artworkId: Int) {\
                    artwork(id: $artworkId) {\
                        keywords {\
                        name\
                        }\
                    }\
                }'
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={'artworkId': artwork.id})
        assert result.data['artwork']['keywords'][0]['name'] == "mythe"
        assert result.data['artwork']['keywords'][1]['name'] == "société"
        self.assertIsNone(result.errors)
