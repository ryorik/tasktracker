from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import User, Step, Action
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import addToQueue
import pika
import json
from django.core.serializers.json import DjangoJSONEncoder

from .serializers import ActionSerializer, UserSerializer

def index(request):
    user_list = User.objects.all()
    step_list = Step.objects.all()
    return render(request, './tasktracker/user_list.html', {
        'user_list': user_list,
        'step_list': step_list
    })


class UserCreateView(CreateView):
    model = User
    fields = ('name', 'email', 'registration_date')    

class ActionView(APIView):
    def get(self, request):
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        return Response({"actions": serializer.data})
        

    def post(self, request):
        action = request.data.get('action')        
        serializer = ActionSerializer(data=action)
        if serializer.is_valid(raise_exception=True):
            action_saved = serializer.save()            
            addToQueue.delay(action_saved.id)              
        return Response({"success": "Action '{}' created successfully".format(action_saved.id)})

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})
        

    def post(self, request):
        user = request.data.get('user')    
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({"success": "User '{}' created successfully".format(user_saved.id)})
