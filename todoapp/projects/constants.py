from enum import StrEnum

MAX_PROJECTS_PER_USER = 2

class ValidationError(StrEnum):
    USERS_IDS_MINIMUM_LIMIT = "At least 1 one user must be provided.",
    USERS_IDS_MAXIMUM_LIMIT = "More than 100 users cannot be added at once."

class MemberAddError(StrEnum):
    USER_DOES_NOT_EXIST = "Failed: User does not exist."
    USER_ALREADY_MEMBER = "Skipped: User is already a member of this project."
    USER_MAX_PROJECT_LIMIT = f"Failed: User cannot be a member of more than {MAX_PROJECTS_PER_USER} projects."
    PROJECT_MAX_LIMIT = ("Failed: Project has reached its maximum limit of {limit} members.")
    ADDED_SUCCESSFULLY = "Success: Added to project successfully."

class MemberRemoveError(StrEnum):
    USER_DOES_NOT_EXIST = "Failed: User does not exist."
    USER_IS_NOT_MEMBER = "Skipped: User is not a member of this project."
    REMOVED_SUCCESSFULLY = "Success: User Removed from project successfully."
