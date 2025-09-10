from rest_framework import serializers
from .models import UserId, Treino, Workout
from django.contrib.auth.models import User

class UserIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserId
		fields = ['id_user']

class WorkoutSerializer(serializers.ModelSerializer):
	class Meta:
		model = Workout
		fields = '__all__'

class TreinoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Treino
		fields = '__all__'