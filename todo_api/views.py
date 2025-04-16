from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view
import datetime

errorMsg = "Something went wrong!"

@api_view(['GET'])
def todoList(request):
    try:
        todos_not_completed = Todo.objects.filter(completed=False).order_by('created_at')
        todos_completed = Todo.objects.filter(completed=True).order_by('-created_at')

        not_completed_serializer = TodoSerializer(todos_not_completed, many=True)
        completed_serializer = TodoSerializer(todos_completed, many=True)

        return Response({
            "ongoing": not_completed_serializer.data,
            "completed": completed_serializer.data
        }, status=status.HTTP_200_OK)
    except:
        return Response(
            {"message": errorMsg},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def todoItem(request, pk):
    try:
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            {"message": errorMsg},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def todoCreate(request):
    try:
        data = {
            'task': request.data.get('task'), 
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            {"message": errorMsg}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
def todoUpdate(request, pk):
    try:
        todo = Todo.objects.get(id=pk)            
        data = {
            'updated_at': datetime.datetime.now(), 
        }
        if request.data.get('task') is not None:
            data['task'] = request.data.get('task')
        if request.data.get('completed') is not None:
            data['completed'] = request.data.get('completed')
            
        serializer = TodoSerializer(instance = todo, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            {"message": errorMsg}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['DELETE'])
def todoDelete(request, pk):
    try:
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    except:
        return Response(
            {"message": errorMsg}, 
            status=status.HTTP_400_BAD_REQUEST
        )