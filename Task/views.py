from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskSerializer
from .models import Task

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):

    data = request.data.copy()
    data['user'] = request.user.id

    task = TaskSerializer(data = data)
    if task.is_valid():
        task.save(user = request.user)
        return Response(task.data, status=status.HTTP_201_CREATED)
    else:
        return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    tasks = Task.objects.filter(user = request.user)
    serializer = TaskSerializer(tasks, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, pk):
    try:
        task = Task.objects.get(pk = pk, user = request.user)
    except Task.DoesNotExist:
        return Response({'error': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)




