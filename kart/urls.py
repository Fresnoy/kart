from django.contrib import admin
from django.urls import path, include

from kart import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('people/', include('people.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
