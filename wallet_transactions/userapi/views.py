from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    """Create view for register user with method post"""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """Method post with serialized data check valid and create user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }
        )
