from django.http import JsonResponse
from kart.schema import schema
from django.views import View


class Artwork25ViewGQL(View):

    def get(self, request, *args, **kwargs):

        query = '''
        {
  artworks {
    ...on FilmType{
      title
    }
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
      picture
    }
    inSituGalleries{
      picture
    }
    authors {
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
      title
    }
    artworks {
      id
    }
    partners {
      name
      taskLabel
    }
    prevArtwork
    nextArtwork
  }
}
        '''

        result = schema.execute(query)

        if result.errors:
            return JsonResponse({'errors': [str(error) for error in result.errors]}, status=400)

        return JsonResponse(result.data, status=200)

# {
#   artworks {
#     title
#     picture
#     #audioLink
#     #videoLink
#     type
#     descriptionShortFr
#     descriptionShortEn
#     descriptionFr
#     descriptionEn
#     thanksFr
#     thanksEn
#     processGalleries{
#     	media{
#       	picture
#       }

#     }
#     teaserGalleries {
#       id
#     }
#     authors {
#       firstName
#       lastName
#       nickname
#       bioShortFr
#       bioShortEn
#       bioFr
#       bioEn
#     }
#     diffusion {
#       id
#       title
#     }
#     artworks {
#       id
#     }
#     partners {
#       name
#       taskLabel
#     }
#     #prevArtwork
#     #nextArtwork
#   },
#   artworks{
#       teaserGalleries {
#         id
#       }
#     }
# 	}
