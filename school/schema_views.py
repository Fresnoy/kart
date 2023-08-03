from django.http import JsonResponse
from kart.schema import schema
from django.views import View


class PromotionViewGQL(View):

    def get(self, request, *args, **kwargs):

        query = '''
        {
            promotions {
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

        query = '''
        {
        students {
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
                name
                startingYear
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
