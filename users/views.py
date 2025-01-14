from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

#class UserMeView(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     user = request.user
    #     return Response({
    #         "username": user.username,
    #         "email": user.email,
    #     })



# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

