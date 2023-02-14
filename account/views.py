from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from account.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = get_user_model()
    serializer_class = UserSerializer
