from rest_framework import viewsets
from repository import models
from .rest_serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all()    #取数据
    serializer_class = UserSerializer           # 交给类序列化