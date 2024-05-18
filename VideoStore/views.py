from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import VideoProject
from .serializers import VideoProjectSerializer
import json
from django.shortcuts import render

from .tasks import add
from celery.result import AsyncResult

from .tasks import generate_thumbnails

def add_view(request):
    result = add.delay(4, 4)
    return Response({'task_id': result.id})

def check_task_status(task_id):
    result = AsyncResult(task_id)
    return result.status, result.result


# class VideoProjectListCreate(generics.ListCreateAPIView):
#     queryset = VideoProject.objects.all()
#     serializer_class = VideoProjectSerializer
#     # permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         form = VideoProjectForm(request.data, request.FILES)
#         if form.is_valid():
#             video_project = form.save()
#             serializer = VideoProjectSerializer(video_project)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# class VideoProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = VideoProject.objects.all()
#     serializer_class = VideoProjectSerializer
#     # permission_classes = [IsAuthenticated]

def home(request):
    return render(request,'home.html')


@api_view(['POST'])
def upload_file(request):
    data = request.data
    print(data)
    serializer = VideoProjectSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        result = generate_thumbnails.delay(serializer.data['video'])

        return Response({
            'status':200,
            'message' : 'uploaded',
            'task_id': result.id,
        })
    
    return Response({
        'status' : 400,
        'message' : serializer.errors,
    })

@api_view(['POST'])
def fetch_file(request):
    data = request.data
    task_id = data.get('task_id')
    if not task_id:
        return Response({
            'status': 400,
            'message': 'Task ID is required.',
        })
    print(data,task_id)
    status, result = check_task_status(task_id)
    print(status,result)
    if status=="SUCCESS":
        return Response({
            'status':200,
            'message' : 'fetched',
            'images': result,
        })
    
    return Response({
        'status' : 400,
        'message':"Task is still processing.",
    })