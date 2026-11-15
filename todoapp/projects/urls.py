from django.urls import path

from projects.views import ProjectMemberApiView

urlpatterns = [
    path(
        "projects/<int:pk>/members/",
        ProjectMemberApiView.as_view(),
        name="project-members",
    ),
]
