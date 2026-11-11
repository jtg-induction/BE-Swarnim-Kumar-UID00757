from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email']

class TodoStatsSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'completed_count', 
            'pending_count'
        ]

class UserPendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'pending_count'
        ]

class UserWiseProjectSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )
    in_progress_projects = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )
    completed_projects = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'to_do_projects',
            'in_progress_projects',
            'completed_projects'
    ]
