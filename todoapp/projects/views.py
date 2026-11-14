from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from projects.constants import MAX_PROJECTS_PER_USER, MemberAddError, MemberRemoveError
from projects.models import Project, ProjectMember
from projects.serializers import ProjectAddMemberSerializer

User = get_user_model()

class ProjectMemberApiView(GenericAPIView):
    """
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """
    queryset = Project.objects.all()
    serializer_class = ProjectAddMemberSerializer
    permission_classes = [permissions.IsAdminUser]

    # @action(detail=True, methods=["post"], url_path="members")
    def post(self, request, pk=None):
        project_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = serializer.validated_data["user_ids"]
        logs = {}
        memberships_to_create = []

        with transaction.atomic():
            project = Project.objects.select_for_update().get(pk=project_obj.pk)

            existing_member_ids = ProjectMember.objects.filter(
                project=project
            ).values_list("member_id", flat=True)
            remaining_slots = project.max_members - len(existing_member_ids)

            users_mapped = {
                u.id: u
                for u in User.objects.select_for_update()
                .filter(id__in=user_ids)
            }

            project_counts = dict(
                ProjectMember.objects.filter(
                    member_id__in=users_mapped.keys())
                    .values_list("member_id")
                    .annotate(count=Count("id")
                )
            )

            for uid in user_ids:
                user = users_mapped.get(uid)

                if not user:
                    logs[str(uid)] = MemberAddError.USER_DOES_NOT_EXIST
                    continue

                if uid in existing_member_ids:
                    logs[str(uid)] = MemberAddError.USER_ALREADY_MEMBER
                    continue

                if project_counts.get(uid, 0) > MAX_PROJECTS_PER_USER:
                    logs[str(uid)] = MemberAddError.USER_MAX_PROJECT_LIMIT
                    continue

                if remaining_slots <= 0:
                    logs[str(uid)] = MemberAddError.PROJECT_MAX_LIMIT.format(limit=project.max_members)
                    continue

                memberships_to_create.append(
                    ProjectMember(project=project, member=user)
                )
                remaining_slots -= 1
                logs[str(uid)] = MemberAddError.ADDED_SUCCESSFULLY

            if memberships_to_create:
                ProjectMember.objects.bulk_create(memberships_to_create)

        return Response({"logs": logs})

    # @add_members.mapping.patch
    def patch(self, request, pk=None):
        project_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = serializer.validated_data["user_ids"]
        logs = {}
        memberships_to_remove = []

        project = Project.objects.get(pk=project_obj.pk)

        existing_member_ids = ProjectMember.objects.filter(project=project).values_list("member_id", flat=True)
        existing_user_ids = User.objects.filter(id__in=user_ids).values_list("id", flat=True)

        for uid in user_ids:
            if uid not in existing_user_ids:
                logs[str(uid)] = MemberRemoveError.USER_DOES_NOT_EXIST
                continue

            if uid not in existing_member_ids:
                logs[str(uid)] = MemberRemoveError.USER_IS_NOT_MEMBER
                continue

            memberships_to_remove.append(uid)
            logs[str(uid)] = MemberRemoveError.REMOVED_SUCCESSFULLY

        if memberships_to_remove:
            ProjectMember.objects.filter(
                project=project, member_id__in=memberships_to_remove
            ).delete()

        return Response({"logs": logs})
        
