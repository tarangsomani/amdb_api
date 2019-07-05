from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
#from rest_framework.Response import Response
from django.http import HttpResponse


@api_view(['POST'])
def create_user(request):

    name = request.data['name']
    username = request.data['username']
    password = request.data['password']
    short_bio = request.data['short_bio']

    if name is None or len(name) == 0:
        return HttpResponse('error_message:Name cannot be empty',status=400)

    #if username is None or len(username) > 0:
    if password is None or len(password) < 6:
        return HttpResponse("password should be greater than 6")

    return HttpResponse("hey its me")

