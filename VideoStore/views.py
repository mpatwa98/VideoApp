from django.shortcuts import render

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import VideoProjectSerializer

from celery.result import AsyncResult
from .tasks import generate_thumbnails

def home(request):
    return render(request,'home.html')


def check_task_status(task_id):
    result = AsyncResult(task_id)
    return result.status, result.result


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    if not [IsAuthenticated]:
        return Response({
            'status':201,
            'message' : 'not authenticated',
        })
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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