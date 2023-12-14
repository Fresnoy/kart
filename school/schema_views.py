from django.http import JsonResponse
from kart.schema import schema
from django.views import View
from graphql_jwt.utils import get_user_by_payload, get_credentials, get_payload


class PromotionViewGQL(View):

    def get(self, request, *args, **kwargs):

        # Promotion id
        id = kwargs.get('id')

        # if an id is provided, get data for that promotion ...
        if id:
            query = "{ promotion(id: " + str(id) + ")"
        # ... otherwise display all Promotions
        else:
            query = "{ promotions"

        query += '''
            {
                id
                name
                startingYear
                endingYear
                picture
                students {
                    id
                    firstName
                    lastName
                    nickname
                    displayName
                    nationality
                }
            }
        }
        '''

        result = schema.execute(query)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)


class StudentViewGQL(View):

    def get(self, request, *args, **kwargs):
        # Student id
        id = kwargs.get('id')

        # if an id is provided, get data for that student ...
        if id:
            query = "{ student(id: " + str(id) + ")"
        # ... otherwise display all students
        else:
            query = "{ students"

        query += '''{
            id
            firstName
            lastName
            photo
            gender
            nationality
            birthdate
            firstName
            lastName
            nationality
            birthdate
            birthplace
            birthplaceCountry
            cursus
            bioShortFr
            bioShortEn
            bioFr
            bioEn
            promotion{
                id
                name
                startingYear
                endingYear
            }
            websites {
            titleFr
            titleEn
            url
            }
            artworks{
            id
            title
            picture
            type
            }
        }
        }'''

        result = schema.execute(query)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)


class TeachinArtistListViewGQL(View):
    """ List the teaching artists by year"""

    def get(self, request, *args, **kwargs):
        query = '''
            query teachingArtistList{
                teachingArtistsList{
                    year
                    teachers{
                        id
                        firstName
                        lastName
                        nickname
                        displayName
                        photo
                    }
                },
            }
            '''

        result = schema.execute(query)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)


class TeachingArtistGQL(View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        query = '''
        query teachingArtist($id: Int) {
            teachingArtist(id: $id){
                id
                firstName
                lastName
                nickname
                photo
                birthdate
                birthplace
                birthplaceCountry
                bioShortFr
                bioShortEn
                bioFr
                bioEn
                presentationTextFr
                presentationTextEn
                years
                picturesGallery {
                    media {
                        label
                        picture
                    }
                }
                diffusions {
                id
                artwork {
                    title
                }
                event {
                    title
                    startingDate
                    place {
                    name
                    city
                    country
                    }
                }
                }
            },
        }
        '''

        context = {}
        result = schema.execute(
            query, variables={'id': id}, context=context)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)


class CandidatureResultsGQL(View):

    def get(self, request, *args, **kwargs):
        query = '''
            query {
                Campaign : studentApplicationSetup(isCurrentSetup: true) {
                    informationAndTourDate
                    interviewsEndDate
                    interviewsPublishDate
                    interviewsStartDate
                    dateOfBirthMax
                    candidatureDateStart
                    candidatureDateEnd
                    selectedPublishDate
                    promotion {
                      id
                      name
                      startingYear
                      endingYear
                    }
                }
                ITWselected : studentApplicationAdmins(application_Campaign_IsCurrentSetup: true,
                                                       selectedForInterview: true) {
                    edges {
                        node {
                            id
                            selected
                            waitListed
                            positionInWaitlist
                            selectedForInterview
                            positionInInterviewWaitlist
                            interviewDate
                            application {
                                remoteInterview
                                binomialApplicationWith
                                artist {
                                    displayName
                                    lastName
                                    birthdate
                                    gender
                                    motherTongue
                                    otherLanguage
                                    photo
                                    nationality
                                }
                            }
                        }
                    }
                }
                ITWonwaitlist : studentApplicationAdmins(application_Campaign_IsCurrentSetup: true,
                                                         waitListedForInterview: true) {
                    edges {
                        node {
                            id
                            selected
                            waitListed
                            positionInWaitlist
                            selectedForInterview
                            positionInInterviewWaitlist
                            interviewDate
                            application {
                                remoteInterview
                                binomialApplicationWith
                                artist {
                                    displayName
                                    lastName
                                    birthdate
                                    gender
                                    motherTongue
                                    otherLanguage
                                    photo
                                    nationality
                                }
                            }
                        }
                    }
                }
                Selected : studentApplicationAdmins(application_Campaign_IsCurrentSetup: true, selected: true) {
                    edges {
                        node {
                            id
                            selected
                            waitListed
                            positionInWaitlist
                            selectedForInterview
                            positionInInterviewWaitlist
                            interviewDate
                            application {
                                remoteInterview
                                binomialApplicationWith
                                artist {
                                    displayName
                                    lastName
                                    birthdate
                                    gender
                                    motherTongue
                                    otherLanguage
                                    photo
                                    nationality
                                }
                            }
                        }
                    }
                }
                Selectedonwaitlist : studentApplicationAdmins(application_Campaign_IsCurrentSetup: true,
                                                              waitListed: true) {
                    edges {
                        node {
                            id
                            selected
                            waitListed
                            positionInWaitlist
                            selectedForInterview
                            positionInInterviewWaitlist
                            interviewDate
                            application {
                                remoteInterview
                                binomialApplicationWith
                                artist {
                                    displayName
                                    lastName
                                    birthdate
                                    gender
                                    motherTongue
                                    otherLanguage
                                    photo
                                    nationality
                                }
                            }
                        }
                    }
                }
            }
            '''

        # get user by token
        credential = get_credentials(request)
        payload = get_payload(credential)
        user = get_user_by_payload(payload)
        # replace user in request (why?)
        request.user = user
        result = schema.execute(query, context_value=request)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)
