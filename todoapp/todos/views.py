from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from todos.models import Todo
from todos.serializers import TodoAPISerializer

class StandardTodoResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    
    serializer_class = TodoAPISerializer
    pagination_class = StandardTodoResultsPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
