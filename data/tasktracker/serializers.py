from rest_framework import serializers
from .models import Action, Step, User


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
    

    def create(self, validated_data):        
        return Action.objects.create(**validated_data) 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    

    def create(self, validated_data):
        return User.objects.create(**validated_data) 