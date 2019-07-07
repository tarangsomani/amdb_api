from rest_framework.serializers import ModelSerializer
from users.models import Users
from rest_framework import serializers


class UserSerializer(ModelSerializer):

   # name = serializers.CharField(required=True)
   # username = serializers.CharField(required=True)

    class Meta:
        model = Users
        fields = ['id','name','username','short_bio','created_on','updated_on']