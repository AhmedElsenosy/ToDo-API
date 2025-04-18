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
