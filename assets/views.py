import json

from django.http import HttpResponse

from rest_framework import viewsets, permissions
from rest_framework_jwt.settings import api_settings

from .models import Gallery, Medium
from people.models import User
from school.models import StudentApplicationSetup

from .serializers import GallerySerializer, MediumSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


def vimeo_get_upload_token(request):

    # make sur user is auth
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
            setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
            vimeo = {
                'name': setup.video_service_name,
                'url': setup.video_service_url,
                'token': setup.video_service_token
            }

            return HttpResponse(json.dumps(vimeo))

    return HttpResponse("Not Authenticated")
