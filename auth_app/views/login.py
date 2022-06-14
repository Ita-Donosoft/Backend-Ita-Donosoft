from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from core.serializers import user_serializers


class Login(ObtainAuthToken):
    user_serializer_class = user_serializers.UserSerializer

    def post(self, request):
        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if not login_serializer.is_valid():
            return Response({'erros': login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = login_serializer.validated_data['user']

        if not user.is_active:
            return Response({'error': 'The user is not enable to login'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        user_serializer = self.user_serializer_class(user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        return Response({
            'data': {'token': token.key,
                     'user': user_serializer.data}
        }, status=status.HTTP_200_OK)
