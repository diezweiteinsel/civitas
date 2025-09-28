from backend.models import Form, Application
from backend.models.domain.user import User


_global_applications_db: list[Application] = []
_global_forms_db: list[Form] = []
_global_users_db: list[User] = []
