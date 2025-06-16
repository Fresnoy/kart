from django.test import TestCase

import graphene

from kart.schema import Query

from school.tests.factories import (
    ArtistFactory,
    StudentFactory,
    TeachingArtistFactory,
    ScienceStudentFactory,
    VisitingStudentFactory
)


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

    def test_query_specific_artists(self):
        ArtistFactory(id="1", nickname="John Doe", artist_photo="jdoe.jpg")

        query = 'query FetchArtists {\
                    artists {\
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
                    artists(isStudent: true) {\
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
                    artists(isStudent: true) {\
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
                    artists(isTeacher: true) {\
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
                    artists(isTeacher: true) {\
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
                    artists(isScienceStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                student {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artists'][0]['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['displayName'] == "John Doe"
        assert result.data['artists'][0]['student']['scienceStudent']['student']['displayName'] is not None

    def test_query_artists_no_filter_also_student_but_not_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                student {\
                                    displayName\
                                }\
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
                    artists(isScienceStudent: true) {\
                        displayName\
                        student {\
                            displayName\
                            scienceStudent {\
                                student {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        print(result.errors)

        assert result.data['artists'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_filter_also_visiting_student(self):
        artist = ArtistFactory(nickname="John Doe")
        VisitingStudentFactory(artist=artist)

        query = 'query FetchArtists {\
                    artists(isVisitingStudent: true) {\
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
                    artists(isVisitingStudent: true) {\
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

    # Following tests about artist pagination filter
    def test_query_artists_pagination_filter_also_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isStudent: true) {\
                     edges {\
                            node {\
                                displayName\
                                student {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'][0]['node']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['student']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_not_student(self):
        ArtistFactory(nickname="John Doe")

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isStudent: true) {\
                     edges {\
                            node {\
                                displayName\
                                student {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_also_teacher(self):
        artist = ArtistFactory(nickname="John Doe")
        TeachingArtistFactory(artist=artist)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isTeacher: true) {\
                        edges {\
                            node {\
                                displayName\
                                teacher {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'][0]['node']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['teacher']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_not_teacher(self):
        ArtistFactory(nickname="John Doe")

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isTeacher: true) {\
                        edges {\
                            node {\
                                displayName\
                                teacher {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_also_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        student = StudentFactory(artist=artist)
        ScienceStudentFactory(student=student)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isScienceStudent: true) {\
                        edges {\
                            node {\
                                displayName\
                                student {\
                                    displayName\
                                    scienceStudent {\
                                        id\
                                    }\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'][0]['node']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['student']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['student']['scienceStudent']['id'] is not None
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_no_filter_also_student_but_not_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "") {\
                        edges {\
                            node {\
                                displayName\
                                student {\
                                    displayName\
                                    scienceStudent {\
                                        id\
                                    }\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'][0]['node']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['student']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['student']['scienceStudent'] is None
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_also_student_but_not_science_student(self):
        artist = ArtistFactory(nickname="John Doe")
        StudentFactory(artist=artist)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isScienceStudent: true) {\
                        edges {\
                            node {\
                                displayName\
                                student {\
                                    displayName\
                                    scienceStudent {\
                                        id\
                                    }\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'] == []
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_also_visiting_student(self):
        artist = ArtistFactory(nickname="John Doe")
        VisitingStudentFactory(artist=artist)

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isVisitingStudent: true) {\
                        edges {\
                            node {\
                                displayName\
                                visitingStudent {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'][0]['node']['displayName'] == "John Doe"
        assert result.data['artistsPagination']['edges'][0]['node']['visitingStudent']['displayName'] == "John Doe"
        self.assertIsNone(result.errors)

    def test_query_artists_pagination_filter_not_visiting_student(self):
        ArtistFactory(nickname="John Doe")

        query = 'query artistsPaginationFilters {\
                    artistsPagination(name: "", isVisitingStudent: true) {\
                        edges {\
                            node {\
                                displayName\
                                visitingStudent {\
                                    displayName\
                                }\
                            }\
                        }\
                    }\
                }'

        schema = graphene.Schema(query=Query)
        result = schema.execute(query)

        assert result.data['artistsPagination']['edges'] == []
        self.assertIsNone(result.errors)
