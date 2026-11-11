from django.contrib.auth import get_user_model
from rest_framework import serializers
from todos import models

class TodoCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class TodoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', 
        format="%I:%M %p, %d %b, %Y"
    )
    creator = TodoCreatorSerializer(source='user', read_only=True)

    class Meta:
        model = models.Todo
        fields = ["id", "name", "status", "created_at", "creator"]

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"
    