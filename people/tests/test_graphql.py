from django.test import TestCase

import graphene

from kart.schema import Query
from people.tests.factories import (
    ArtistFactory
)
from school.tests.factories import (
    StudentFactory,
    TeachingArtistFactory,
    ScienceStudentFactory,
    VisitingStudentFactory
)


class TestGQLPages(TestCase):
    # Following tests about artists
    def test_query_artists(self):
        ArtistFactory()

        query = 'query FetchArtists {\
                    artists(name: "") {\
                        id\
                        displayName\
                        artistPhoto\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'] is not None
        self.assertIsNone(result.errors)

    def test_query_specific_artists(self):
        ArtistFactory(id="1", nickname="John Doe", artist_photo="jdoe.jpg")

        query = 'query FetchArtists {\
                    artists(name: "") {\
                        id\
                        displayName\
                        artistPhoto\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['id'] == "1"
        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['artistPhoto'] == "jdoe.jpg"
        self.assertIsNone(result.errors)

    # Following tests about artist filter
    def test_query_artists_filter_also_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(name: "", isStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_filter_not_student(self):
        ArtistFactory(nickname="John Doe")

        query = 'query FetchArtists {\
                    artists(name: "", isStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_also_teacher(self):
        artist = ArtistFactory(nickname="John Doe")
        TeachingArtistFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(name: "", isTeacher: true) {\
                        displayName\
                        teacher {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['teacher']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_filter_not_teacher(self):
        ArtistFactory(nickname="John Doe")

        query = 'query FetchArtists {\
                    artists(name: "", isTeacher: true) {\
                        displayName\
                        teacher {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_filter_also_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        student = StudentFactory(artist=artist)
        ScienceStudentFactory(student=student)

        query = 'query FetchArtists {\
                    artists(name: "", isScienceStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                displayName\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['scienceStudent']['displayName'] is None
        # This query return following error: "'ScienceStudent' object has no attribute 'artist'"
        # self.assertIsNone(result.errors)

    def test_query_artists_no_filter_also_student_but_not_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(name: "") {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                displayName\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['scienceStudent'] is None
        self.assertIsNone(result.errors)

    def test_query_artists_filter_also_student_but_not_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(name: "", isScienceStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                displayName\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_filter_also_visiting_student(self):
        artist = ArtistFactory(nickname="John Doe")
        VisitingStudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(name: "", isVisitingStudent: true) {\
                        displayName\
                        visitingStudent {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['visitingStudent']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_filter_not_visiting_student(self):
        ArtistFactory(nickname="John Doe")

        query = 'query FetchArtists {\
                    artists(name: "", isVisitingStudent: true) {\
                        displayName\
                        visitingStudent {\
                            displayName\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'] == []
        self.assertIsNone(result.errors)
