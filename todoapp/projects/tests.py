from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from projects.constants import ValidationError, MemberAddError, MemberRemoveError
from projects.models import Project, ProjectMember

User = get_user_model()

class ProjectMembershipAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            first_name="Admin",
            last_name="Test",
            email="admin@test.com",
            password="Password123",
            is_staff=True
        )
        cls.user = User.objects.create_user(
            first_name="User",
            last_name="Test",
            email="user@test.com",
            password="Password123"
        )
        cls.admin_token = Token.objects.create(user=cls.admin)
        cls.user_token = Token.objects.create(user=cls.user)

        cls.member_1 = User.objects.create_user(
            first_name="Test",
            last_name="Member 1",
            email="member1@test.com",
            password="Password123"
        )

        cls.member_2 = User.objects.create_user(
            first_name="Test",
            last_name="Member 2",
            email="member2@test.com",
            password="Password123"
        )

        cls.member_3 = User.objects.create_user(
            first_name="Test",
            last_name="Member 3",
            email="member3@test.com",
            password="Password123"
        )

    def setUp(self):
        self.project = Project.objects.create(name="Test Project", max_members=2)
        self.url = reverse("project-members", kwargs={"pk": self.project.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

    def test_add_users_to_project_success(self):
        payload = {"user_ids": [self.member_1.id, self.member_2.id]}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"],
            {
                str(self.member_1.id): MemberAddError.ADDED_SUCCESSFULLY,
                str(self.member_2.id): MemberAddError.ADDED_SUCCESSFULLY,
            },
        )
        
        self.assertEqual(
            ProjectMember.objects.filter(project=self.project).count(), 2
        )
        self.assertTrue(
            ProjectMember.objects.filter(
                project=self.project, member=self.member_1
            ).exists()
        )
        self.assertTrue(
            ProjectMember.objects.filter(
                project=self.project, member=self.member_2
            ).exists()
        )

    def test_add_non_existent_user_returns_error(self):
        non_existent_id = 999999
        payload = {"user_ids": [non_existent_id]}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"],
            {str(non_existent_id): MemberAddError.USER_DOES_NOT_EXIST},
        )
        self.assertEqual(
            ProjectMember.objects.filter(project=self.project).count(), 0
        )

    
    def test_non_admin_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")

        response = self.client.post(
            self.url,
            {"user_ids": [self.member_1.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_request_rejected(self):
        self.client.credentials()

        response = self.client.post(
            self.url,
            {"user_ids": [self.member_1.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_members_enforces_project_max_members_and_logs(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        payload = {
            "user_ids": [
                self.member_1.id,
                self.member_2.id,
            ]
        }

        response = self.client.post(self.url, payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"],
            {
                str(self.member_1.id): MemberAddError.ADDED_SUCCESSFULLY,
                str(self.member_2.id): MemberAddError.ADDED_SUCCESSFULLY,
            },
        )
        
        self.assertEqual(ProjectMember.objects.filter(project=self.project).count(), 2)

    def test_add_member_exceeding_two_project_limit_fails(self):
        p1 = Project.objects.create(name="P1", max_members=5)
        p2 = Project.objects.create(name="P2", max_members=5)
        ProjectMember.objects.create(project=p1, member=self.member_1)
        ProjectMember.objects.create(project=p2, member=self.member_1)

        response = self.client.post(
            self.url,
            {"user_ids": [self.member_1.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"][str(self.member_1.id)],
            "Failed: User cannot be a member of more than 2 projects.",
        )

    def test_empty_user_ids_fails_serializer_validation(self):
        response = self.client.post(self.url, {"user_ids": []}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_non_existent_user_returns_error(self):
        non_existent_id = 999999
        payload = {"user_ids": [non_existent_id]}

        response = self.client.patch(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"],
            {str(non_existent_id): MemberRemoveError.USER_DOES_NOT_EXIST},
        )
    
    def test_remove_members_success_and_skipped_logs(self):
        ProjectMember.objects.create(project=self.project, member=self.member_1)

        response = self.client.patch(
            self.url,
            {"user_ids": [self.member_1.id, self.member_2.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["logs"],
            {
                str(self.member_1.id): MemberRemoveError.REMOVED_SUCCESSFULLY,
                str(self.member_2.id): MemberRemoveError.USER_IS_NOT_MEMBER,
            },
        )
        self.assertFalse(
            ProjectMember.objects.filter(
                project=self.project, member=self.member_1
            ).exists()
        )
