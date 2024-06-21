from rest_framework.generics import CreateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView

from account.serializers import RegisterSerializer, LoginSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer