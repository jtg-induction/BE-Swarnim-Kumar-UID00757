from django.contrib import admin

from projects.models import Project, ProjectMember


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "max_members")
    list_filter = ["status"]

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "member")
    list_select_related = ("project", "member")


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
