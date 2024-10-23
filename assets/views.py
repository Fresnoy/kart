from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Gallery, Medium
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


@api_view(["GET"])
@permission_classes((permissions.IsAuthenticated,))
def vimeo_get_upload_token(request):
    user = request.user
    # send him infos
    if user:
        # get setup infos
        setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        if setup:
            # customize returned infos
            vimeo = {
                "name": setup.video_service_name,
                "url": setup.video_service_url,
                "token": setup.video_service_token,
            }
            return Response(vimeo, status=status.HTTP_200_OK)
        # No setup
        return Response("Setup Empty", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
