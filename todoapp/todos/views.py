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

    def get_queryset(self):
        queryset = Todo.objects.all().order_by('-date_created')

        if self.action == 'list':
            user_id = self.request.data.get('user_id')
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)

        return queryset
