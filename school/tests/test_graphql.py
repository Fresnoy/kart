import pytest
import json

from django.test import TestCase
from django.urls import reverse

import graphene
from urllib.parse import urlencode

from rest_framework import status

from kart.schema import Query
from production.tests.factories import EventFactory, PerformanceFactory
from people.tests.factories import ArtistFactory
from school.tests.factories import PromotionFactory, StudentFactory

class TestGQLPages(TestCase):
    """
    TODO: do tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @pytest.mark.skip()
    def test_page_candidature_results_list(self):
        page = "page/candidatureResultsList"
        # require auth
        pass
    
    # @pytest.mark.skip()
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

    
    def test_query_promotions(self):        
        # create objects
        self.student = StudentFactory()
        # query
        query = 'query {\
                    promotions {\
                    name\
                    picture\
                    startingYear\
                    endingYear\
                    students {\
                        id\
                        displayName\
                    }\
                    }\
                }'
        # execute query
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    @pytest.mark.skip()
    def test_query_studentx(self):
        query = 'query StudentX($etudiantID: Int) {\
                    student(id: $etudiantID) {\
                        displayName\
                        photo\
                        gender\
                        birthdate\
                        birthplace\
                        birthplaceCountry\
                        bioShortFr\
                        bioShortEn\
                        bioFr\
                        bioEn\
                        cursus\
                        promotion {\
                            name\
                            startingYear\
                            endingYear\
                        }\
                        websites {\
                            titleFr\
                            url\
                        }\
                        artworks {\
                            id\
                            title\
                            picture\
                            type\
                            productionDate\
                            diffusion {\
                                event {\
                                    title\
                                    id\
                                }\
                            }\
                        }\
                    }\
                }'
    
    @pytest.mark.skip()
    def test_query_professorx(self):
        query = 'query ProfessorX($professorID: Int) {\
                    teachingArtist(id: $professorID) {\
                        displayName\
                        gender\
                        photo\
                        birthplace\
                        birthplaceCountry\
                        birthdate\
                        presentationTextFr\
                        presentationTextEn\
                        cursus\
                        residenceCountry\
                        residenceTown\
                    }\
                }'
    
    @pytest.mark.skip()
    def test_query_exhibx(self):
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
