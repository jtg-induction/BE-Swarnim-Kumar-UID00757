from django.contrib.auth import get_user_model

from rest_framework import serializers

from projects.constants import ValidationError
from projects.models import Project

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

class ProjectAddMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child = serializers.IntegerField(min_value=1),
        allow_empty = False,
        max_length = 100,
        min_length = 1,
        error_messages = {
            "min_length": ValidationError.USERS_IDS_MINIMUM_LIMIT,
            "max_length": ValidationError.USERS_IDS_MAXIMUM_LIMIT,
            "empty": ValidationError.USERS_IDS_MINIMUM_LIMIT
        }
    )

    def validate_user_ids(self, data):
        return list(dict.fromkeys(data, None))

