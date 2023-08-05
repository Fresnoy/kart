from django.http import JsonResponse
from kart.schema import schema
from django.views import View


class Artworks25ViewGQL(View):

    def get(self, request, *args, **kwargs):
        # artwork id
        id = kwargs.get('id')
        id = 1927
        query = '''
        query exhib($idExhib: Int)
            { exhibition(id: $idExhib) {
        '''

        # if an id is provided, get data for that artwork ...
        if id:
            query += "artwork(id: " + str(id) + ")"
        # ... otherwise display all artworks
        else:
            query += "artworks"

        query += ''' {
              title
              picture
              #audioLink
              #videoLink
              type
              descriptionShortFr
              descriptionShortEn
              descriptionFr
              descriptionEn
              thanksFr
              thanksEn
              processGalleries{
                media {
                  label
                  picture
                }
              }
              inSituGalleries{
                media {
                  label
                  picture
                }
              }
              authors {
                id
                firstName
                lastName
                nickname
                bioShortFr
                bioShortEn
                bioFr
                bioEn
              }
              diffusion {
                id
                event {
                  title
                }
              }
              relArtworks
              partners {
                name
                #taskLabel
              }
              #prevArtwork
              #nextArtwork
            }
          }
          }
        '''
        print("query", query)
        # context = super().get_context_data(**kwargs)
        context = {}
        result = schema.execute(
            query,  variables={'idExhib': 1949}, context=context)

        if result.errors:
            return JsonResponse(
                {'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)
