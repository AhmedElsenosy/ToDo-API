from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import RegisterSerializer, UserSerializer
# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    user = RegisterSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username = data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = make_password(data['password']),
                username = data['email'],
            )
            return Response({'details': 'Account Created Successfully...'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email Already Exists...'}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data 

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if len(new_password) < 8:
        return Response({'error': 'New password have to be 8 chars.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password == old_password:
        return Response({"error": "You heve to enter difrent password."}, status=status.HTTP_400_BAD_REQUEST)

    # if not old_password or not new_password:
    #     return Response({'error': 'Both old password and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()

    return Response({'details': 'Password Changed Successfully...'}, status=status.HTTP_200_OK)