from django.http import JsonResponse
from kart.schema import schema
from django.views import View


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
            },
        }
        '''

        context = {}
        result = schema.execute(
            query, variables={'id': id}, context=context)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)
