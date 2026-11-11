from django.contrib.auth import get_user_model
from rest_framework import serializers
from projects.models import Project
from users.serializers import TodoStatsSerializer

User = get_user_model()

class ProjectMemberReportSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'completed_count', 
            'pending_count'
        ]

class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name', read_only=True)
    report = ProjectMemberReportSerializer(
        source='members', 
        read_only=True, 
        many=True
    )

    class Meta:
        model = Project
        fields = ['project_title', 'report']

