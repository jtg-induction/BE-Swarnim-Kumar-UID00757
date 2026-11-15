from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, ValidationError):
        errors = {
            field: messages[0] if isinstance(messages, list) else messages
            for field, messages in response.data.items()
        }
        message = "Validation failed"
    else:
        if isinstance(response.data, dict) and "detail" in response.data:
            message = str(response.data["detail"])
            errors = None
        else:
            message = str(response.data['error'])
            errors = None

    response.data = {
        "message": message,
        "errors": errors,
    }
    return response
