from backend.businesslogic.services.mockups import _global_users_db, _global_applications_db, _global_forms_db
from backend.businesslogic.services.applicationService import createApplication
from backend.businesslogic.services.formService import createForm
from backend.models.domain.user import UserType
from backend.businesslogic.user import assign_role
from datetime import date
from backend.models import User, Form, Application


Admin=User(id=1, username="admin", date_created=date.today(), hashed_password="admin")
assign_role(Admin, UserType.ADMIN)
Applicant=User(id=2, username="applicant", date_created=date.today(), hashed_password="applicant")
assign_role(Applicant, UserType.APPLICANT)
Reporter=User(id=3, username="reporter", date_created=date.today(), hashed_password="reporter")
assign_role(Reporter, UserType.REPORTER)
_global_users_db.extend([Admin, Applicant, Reporter])

form = createForm(Admin, {"title": "Form 1", "fields": [{"name": "field1", "type": "text"}, {"name": "field2", "type": "number"}]})

createApplication(Applicant, form ,{"field1": "value1", "field2": "value2"})
createApplication(Applicant, form ,{"field1": "value3", "field2": "value4"})
createApplication(Applicant, form ,{"field1": "value5", "field2": "value6"})