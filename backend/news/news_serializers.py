from rest_framework import serializers
from .models import Us, World, Politics, Business

class UsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Us
        fields = '__all__'

class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = '__all__'

class PoliticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politics
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
