from repository import models
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ('password', 'username', 'email', 'nickname')