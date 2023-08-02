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
