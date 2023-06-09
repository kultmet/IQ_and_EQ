from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import IQViewSet, LoginViewSet, EQViewSet

router = DefaultRouter()

router.register(r'login', LoginViewSet, 'login')
router.register(r'iq', IQViewSet, 'iq')
router.register(r'eq', EQViewSet, 'eq')

urlpatterns = [
    path('', include(router.urls)),
]
