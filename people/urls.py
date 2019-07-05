from django.urls import path

from . import views
import kart.settings as settings

from kart.urls import router

router.register(r'users', views.UserViewSet, basename='user')


urlpatterns = [
    path('', views.UserViewSet.as_view({'get': 'list'})),
    # path('us', views.index, name='main-view'),
    # path(f'account/activate/{settings.PASSWORD_TOKEN}',views.activate, name='user-activate'),
    # path('send-emails',  views.UserViewSet, name='send-emails'),
]

# A creuser ...
# from myapp.views import UserViewSet
# from rest_framework.routers import DefaultRouter
#
# urlpatterns = router.urls
