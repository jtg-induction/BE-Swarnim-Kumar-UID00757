from enum import StrEnum

class ValidationErrorMessage(StrEnum):
    EMAIL_REQUIRED = "Email is required"
    INVALID_CREDENTIALS = "Invalid credentials"
