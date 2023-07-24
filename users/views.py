from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from hashlib import sha256
import re

def make_hash(str):
    return sha256(str.encode('utf-8')).hexdigest()


def username_acceptibility(str):
    p = re.compile('[\d\w]+')
    if (p.match(str)):
        return True
    return False

def password_acceptibility(str):
    flag_upper = False
    flag_lower = False
    flag_number = False
    flag_weird = False
    weird_list = ['!', '@', '#', '$', '%', '&', '*']
    for i in range(len(str)):
        if str[i] >= 'a' and str[i] <= 'z':
            flag_lower = True
        if str[i] >= 'A' and str[i] <= 'Z':
            flag_upper = True
        if str[i] >= '0' and str[i] <= '9':
            flag_number = True
        if str[i] in weird_list:
            flag_weird = True
    if flag_upper and flag_lower and flag_number and flag_weird:
        return True
    return False

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GetUser(APIView):
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'

    def get(self, request, format=None):
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            user = User.objects.filter(username=username)
            if len(user) > 0:
                data = UserSerializer(user[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'User Not Found': 'Invalid username.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Username paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class CreateUser(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = make_hash(serializer.data.get('password'))

            if not username_acceptibility(username):
                return Response({'Bad Request': 'Username\'s format is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not password_acceptibility(password):
                return Response({'Bad Request': 'Password\'s format is wrong'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = User.objects.filter(username=username)
            if len(queryset) > 0:
                return Response({'Bad Request': 'A user with this username already exits'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User(username=username, password=password)
                user.save()
                return Response({'Message' : 'Success'}, status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Non proper request'})
    
class CheckPassword(APIView):
    serializer_class = UserSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = make_hash(serializer.data.get('password'))

            queryset = User.objects.filter(username=username) 
            if len(queryset) == 0:
                return Response({'User Not Found': 'Invalid username.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                user = User.objects.filter(username=username).first()

                if user.password == password:
                    return Response({'Message': 'Correct Password'}, status=status.HTTP_200_OK)
                else:
                    return Response({'Bad Request': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'Bad Request': 'Non proper request'})



        

