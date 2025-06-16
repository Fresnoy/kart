import json
import graphene

from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework import status

from utils.tests.factories import UserFactory
from utils.tests.utils import obtain_jwt_token

from kart.schema import Query
from school.tests.factories import (StudentFactory,
                                    TeachingArtistFactory,
                                    StudentApplicationFactory,
                                    ScienceStudentFactory)


class TestGQLPages(TestCase):
    """
    TODO: do tests
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_page_candidature_results_list(self):
        # TEST WITH JWT
        # create value
        StudentApplicationFactory()
        # auth user
        user = UserFactory()
        user.is_staff = True
        user.save()
        jwt = obtain_jwt_token(user)
        # get infos
        candidature_results_list_url = reverse("candidatureResultsList_gql")
        response = self.client.get(candidature_results_list_url, HTTP_AUTHORIZATION="JWT {}".format(jwt["access"]))

        results = json.loads(response.content)
        self.assertFalse(hasattr(results, "errors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_candidature_results_list_with_token(self):
        # TEST WITH TOKEN
        # create value
        StudentApplicationFactory()
        # auth user
        user = UserFactory()
        user.is_staff = True
        user.save()
        token = Token.objects.create(user=user)
        token.save()
        # get infos
        candidature_results_list_url = reverse("candidatureResultsList_gql")
        response = self.client.get(candidature_results_list_url, HTTP_AUTHORIZATION="TOKEN {}".format(token))

        results = json.loads(response.content)
        self.assertFalse(hasattr(results, "errors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query_promotions(self):
        # create objects
        self.student = StudentFactory()
        # query
        query = "query {\
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
                }"
        # execute query
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)

    def test_query_studentx(self):
        self.student = StudentFactory()
        query = "query StudentX($etudiantID: Int) {\
                    student(id: $etudiantID) {\
                        displayName\
                        photo\
                        gender\
                        birthdate\
                        birthplace\
                        birthplaceCountry\
                        deathdate\
                        deathplace\
                        deathplaceCountry\
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
                }"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={"etudiantID": self.student.id})
        self.assertIsNone(result.errors)

    def test_page_teaching_artists_list(self):
        # create value
        TeachingArtistFactory()
        #
        teaching_artists_list_url = reverse("teachingArtistsList_gql")
        response = self.client.get(teaching_artists_list_url)

        teachers = json.loads(response.content)

        self.assertFalse(hasattr(teachers, "errors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query_professorx(self):
        teacher = TeachingArtistFactory()
        query = "query ProfessorX($professorID: Int) {\
                    teachingArtist(id: $professorID) {\
                        displayName\
                        gender\
                        photo\
                        birthplace\
                        birthplaceCountry\
                        birthdate\
                        deathdate\
                        deathplace\
                        deathplaceCountry\
                        presentationTextFr\
                        presentationTextEn\
                        cursus\
                        residenceCountry\
                        residenceTown\
                    }\
                }"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={"professorID": teacher.id})
        self.assertIsNone(result.errors)

    def test_query_sciencestudentx(self):
        science_student = ScienceStudentFactory()
        query = "query ScienceStudentX($scienceStudentID: Int) {\
                    scienceStudent(id: $scienceStudentID) {\
                        student {\
                            id\
                            displayName\
                            photo\
                            gender\
                            birthdate\
                            birthplace\
                            birthplaceCountry\
                            deathdate\
                            deathplace\
                            deathplaceCountry\
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
                        }\
                    }\
                }"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query, variables={"scienceStudentID": science_student.id})
        self.assertIsNone(result.errors)
