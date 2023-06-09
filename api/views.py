from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from api.serializers import (
    CreateEQSerializer,
    CreateIQSerializer,
    CreateTestLoginSerializer,
    RetrieveTestSerializer
)
from testing.models import TestLogin, IQTest, EQTest


class LoginViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CreateTestLoginSerializer
    queryset = TestLogin.objects.all()
    lookup_field = 'login'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveTestSerializer
        return super().get_serializer_class()


class IQViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateIQSerializer
    queryset = IQTest.objects.all()


class EQViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateEQSerializer
    queryset = EQTest.objects.all()
