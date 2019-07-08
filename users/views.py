from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from users.models import Users, AccessToken, Movie
from users.serializers import UserSerializer
from django.contrib.auth.hashers import check_password,make_password


@api_view(['POST'])
def create_user(request):

    name = request.data['name']
    username = request.data['username']
    password = request.data['password']
    short_bio = request.data['short_bio']

    if name is None or len(name) == 0:
        return Response('error_message:Name cannot be empty',status=400)

    if username is None or len(username) == 0:
        return Response("password should be greater than 6",status=400)

    if password is None or len(password) < 6:
        return Response("password should be greater than 6",status=400)

    does_username_exist = Users.objects.filter(username=username).first()
    print('doest username already exist in the db:',does_username_exist)

    if does_username_exist is not None:
        return Response("username already exists!")

    # new_user = Users(name=name,username=username,password=password,short_bio=short_bio)
    # new_user.save()
    new_user = Users.objects.create(name=name,username=username, password=make_password(password), short_bio=short_bio)

    return Response(UserSerializer(instance=new_user).data,status=200)


@api_view(['GET'])
def get_user(request):
    # print (request.query_params['abcd'])
    if 'user_id' in request.query_params:
        user = Users.objects.filter(id=request.query_params['user_id'])
        if len(user)>0:
            return Response(UserSerializer(instance=user[0]).data,status=200)
        else:
            return Response({"error_message":"user not found"})

    else:
        user = Users.objects.all()
        return Response(UserSerializer(instance=user,many=True).data,status=200)

    # return (HttpResponse(True))


@api_view(['POST'])
def user_login(request):

    username = None
    password = None
    if 'username' in request.data:
        username = request.data['username']

    if 'password' in request.data:
        password = request.data['password']

    if not username or not password:
        return Response({"message": "username or password not provided"})

    # check_password have to be used, but i already had some entries so it wont work on them
    user = Users.objects.filter(username=username).first()
    # user will return a list, so we do user[o]
    if user:
        # check password
        if not check_password(password,user.password):
            return Response({"message": "incorrect password or username"})

        else:
            token = AccessToken(user=user)
            token.create_token()
            print (token.access_token)
            token.save()
            return Response({"token":token.access_token},status= 200)

        # return Response(UserSerializer(instance=user).data, status=200)

    else:
        return Response({"message": "incorrect password or username"})


def check_token(token):

    token = AccessToken.objects.filter(token=token)

    if token:
        return token.user

    else:
        return None


@api_view(['POST'])
def create_movie(request):

    if 'username' in request.data:
        username = request.data['username']

    name = request.data['name']
    duration = request.data['duration']
    rate = request.data['rate']

    user = Users.objects.filter(username=username).first()
    # user = user.id

    # to check if the user have already reviewed this movie or not
    old_movie = Movie.objects.filter(name=name,user_id=user.id).first()
    if old_movie is None:
        # checking whether user is logged in
        access_granted = AccessToken.objects.filter(user_id=user.id)

        if access_granted.count() > 0:

            if access_granted[0].is_valid is True:

                # creating a new entry in movie table
                newmovie = Movie.objects.create(name=name,duration_in_minutes = duration,user_id=user.id,overall_rating=rate)
                return Response({'message':'your post is created'})

        else:
            return Response({'message':'Not logged in, not authorized'},status=400)

    else:
        return Response({"message":"you have already reviewed this movie!!"})


@api_view(['POST'])
def user_logout(request):

    access_token = request.META["HTTP_TOKEN"]
    access_granted = AccessToken.objects.filter(access_token=access_token).first()
    if access_granted.is_valid is True:
        access_granted.is_valid = False
        access_granted.save()
        return Response({"message":"you have successfully logged out"},status=200)

    else:
        return Response({"message":"wrong access_token"},status=400)




