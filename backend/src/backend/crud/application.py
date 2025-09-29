


from sqlalchemy import inspect
from sqlalchemy.orm import Session


from backend.core import db
from backend.crud import dbActions
from backend.models.domain.application import Application

from backend.crud import formCrud

from backend.crud.dbActions import getRowsByFilter

def get_application_table_by_id(id):
    applicationTableName = "form_" + str(id)
    Base = db.get_base(True)
    try:
        applicationTable = Base.classes[applicationTableName]
        return applicationTable
    except Exception:
        raise Exception("The table id doesn't exist")


def getRowJsonPayload(applicationTable, row):
    columnNames = [c.key for c in inspect(applicationTable).columns]
    standardColumns = ["id", "user_id", "form_id", "status", "created_at", "current_snapshot_id", "previous_snapshot_id", "is_public"]
    blockColumns = []
    for columnName in columnNames:
        if columnName not in standardColumns:
            blockColumns.append(columnName)
    jsonDict = {}
    for blockColumn in blockColumns:
        jsonDict[blockColumn] = getattr(row, blockColumn)
    return jsonDict

def rowToApplication(row, applicationTable = None) -> Application:
    if not applicationTable:
        applicationTable = get_application_table_by_id(row.form_id)
    jsonPayload = getRowJsonPayload(applicationTable=applicationTable, row=row)


    application = Application(
        id=row.id,
        user_id=row.user_id,
        form_id=row.form_id,
        status= row.status,
        created_at = row.created_at,
        currentSnapshotID= row.current_snapshot_id,
        previousSnapshotID= row.previous_snapshot_id,
        jsonPayload= jsonPayload,
        is_public= row.is_public
    )
    return application

def get_application_by_id(session: Session, form_id:int, app_id: int):

    applicationTable = get_application_table_by_id(form_id)


    applicationRow = dbActions.getRowById(session=session, tableClass=applicationTable, id=app_id)
    return rowToApplication(applicationTable = applicationTable, row = applicationRow)

def get_all_applications_of_type(session: Session, form_id: int) -> list[Application]:
    applicationTable = get_application_table_by_id(form_id)
    applications: list[Application] = []

    allRows = dbActions.getRows(session, applicationTable)

    for row in allRows:
        applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    
    return applications

def get_all_applications(session: Session) -> list[Application]:
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applications_of_type = get_all_applications_of_type(session, form.id)
        applications.extend(applications_of_type)

    return applications


def get_all_public_applications(session: Session) -> list[Application]:
    """
    Returns all applications that are marked as public.
    
    ARGS:
        session (Session): SQLAlchemy session object.
    
    RETURNS:
        list[Application]: List of public Application objects.
    """
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applications_of_type = get_all_applications_of_type(session, form.id)
        applications.extend(applications_of_type)
    public_applications : list[Application] = []
    for application in applications:
        if application.is_public:
            public_applications.append(application)
    return public_applications

def insert_application(session:Session, application: Application):
    applicationTable = get_application_table_by_id(id = application.form_id)
    application_in_db = applicationTable(   
        user_id =application.user_id,
        form_id = application.form_id,
        status = application.status,
        created_at = application.created_at,
        current_snapshot_id = application.currentSnapshotID,
        previous_snapshot_id = application.previousSnapshotID
        )
    for key, value in application.jsonPayload.items():
        setattr(application_in_db, key, value)
    return dbActions.insertRow(session, applicationTable, application_in_db)

# wrapper for updating application status
def updateApplicationStatus(session: Session, tableClass: type, id: int, newStatus: str):
    if newStatus not in ["PENDING", "APPROVED", "REJECTED", "REVISED"]:
        raise ValueError("Invalid status")
    return dbActions.updateRow(session, tableClass, {"id": id, "status": newStatus})