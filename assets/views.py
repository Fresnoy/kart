from rest_framework import viewsets, permissions
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework_jwt.settings import api_settings

from .models import Gallery, Medium
from people.models import User

from .serializers import GallerySerializer, MediumSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


def vimeoUpload(request):
    print("vimeoUpload")
    if(request.META.get('HTTP_AUTHORIZATION')):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        infos = jwt_decode_handler(token)

        user = infos
        try:
            user = User.objects.get(pk=infos['user_id'])
        except User.DoesNotExist:
            user = None

        if(user):
            return HttpResponse(user)

    return HttpResponse("Not Authenticated")
