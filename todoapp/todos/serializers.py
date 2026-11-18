from django.contrib.auth import get_user_model

from rest_framework import serializers

from todos import models
from todos.constants import TODO_TIME_FORMAT, TODO_STATUS_DONE, TODO_STATUS_TO_DO

class TodoCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class TodoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', 
        format=TODO_TIME_FORMAT
    )
    creator = TodoCreatorSerializer(source='user', read_only=True)

    class Meta:
        model = models.Todo
        fields = ["id", "name", "status", "created_at", "creator"]

    def get_status(self, obj):
        return TODO_STATUS_DONE if obj.done else TODO_STATUS_TO_DO
