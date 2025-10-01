


from copy import deepcopy
import json
from sqlalchemy import inspect
from sqlalchemy.orm import Session


from backend.core import db
from backend.crud import dbActions
from backend.models.domain.application import Application, Snapshots

from backend.crud import formCrud

from backend.crud.dbActions import getRowsByFilter

from backend.models.domain.application import ApplicationStatus

def get_application_table_by_id(id):
    """
    Takes:\n
    An id, specifying which form's applicationTable class to retrieve\n
    Returns:\n
    The form's applicationTable class
    """
    applicationTableName = "form_" + str(id)
    Base = db.get_base(True)
    try:
        applicationTable = Base.classes[applicationTableName]
        return applicationTable
    except Exception:
        raise Exception("The table id doesn't exist")


def getRowJsonPayload(row):
    """
    Takes:\n
    A "row" from an applicationTable, which is the same as an instance of that applicationTable class\n
    Returns:\n
    The "jsonPayload" of the "Application" instance which is saved in the given row
    """
    applicationTable = get_application_table_by_id(row.form_id)
    columnNames = [c.key for c in inspect(applicationTable).columns]
    standardColumns = ["id", "user_id", "form_id", "admin_id","status", "created_at", "snapshots", "is_public"]
    blockColumns = []
    for columnName in columnNames:
        if columnName not in standardColumns:
            blockColumns.append(columnName)
    jsonDict = {}
    count = 1
    for blockColumn in blockColumns:
        jsonDict[str(count)] = {"label": blockColumn, "value": getattr(row, blockColumn)}
        count += 1
    return jsonDict

def rowToApplication(row, applicationTable = None) -> Application:
    """
    Takes:\n
    A "row" from an applicationTable, which is the same as an instance of that applicationTable class\n
    Returns:\n
    The "Application" instance which is saved in the given row
    """
    if not applicationTable:
        applicationTable = get_application_table_by_id(row.form_id)
    jsonPayload = getRowJsonPayload(row=row)


    application = Application(
        id=row.id,
        user_id=row.user_id,
        form_id=row.form_id,
        admin_id = row.admin_id,
        status= row.status,
        created_at = row.created_at,
        snapshots= Snapshots.from_json(row.snapshots),
        jsonPayload= jsonPayload,
        is_public= row.is_public
    )
    return application

def get_application_by_id(session: Session, form_id:int, app_id: int):
    """Takes:\n
    A session\n
    A "form_id" specifying of which form to retrieve an application\n
    A "app_id" specifying which application to retrieve from the form

    Returns:\n
    The "Application" instance from the form
    """
    applicationTable = get_application_table_by_id(form_id)


    applicationRow = dbActions.getRowById(session=session, tableClass=applicationTable, id=app_id)
    return rowToApplication(applicationTable = applicationTable, row = applicationRow)


def get_all_global_revisions_of_type(session: Session, form_id: int) -> list[Application]:
    """
    Takes:\n
    A session\n
    A "form_id", specifying of which form to retrieve all global revisions\n

    Returns:\n
    A list of all "Application" instances of the form which's id was given, which are global revisions (nextSnapshotID != null)
    """
    applicationTable = get_application_table_by_id(form_id)
    applications: list[Application] = []
    
            

    allRows = dbActions.getRows(session, applicationTable)
    for row in allRows:
        applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    
    return applications

def get_all_revisions_of_application(session: Session, form_id: int, app_id: int) -> list[Application]:
    """
    Takes a requestapp with form_id and an app_id, returns that exact match plus all revisions,
    meaning those applications with matching form_id where currentSnapshotID == requestapp.app_id
    
    Takes:\n
    A session\n
    A "form_id", specifying of which form to retrieve all revisions\n
    An "app_id", specifying of which application to retrieve all revisions

    Returns:\n
    A list of all "Application" instances of the form which's id was given, which are revisions of the application which's id was given (nextSnapshotID != null)
    """
    applicationTable = get_application_table_by_id(form_id)
    applications: list[Application] = []

    allRows = dbActions.getRows(session, applicationTable)
    for row in allRows:
        if row.id == app_id or get_current_snapshot_id(row.snapshots) == app_id:
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    
    return applications

def get_all_sibling_revisions_of_application(session: Session, form_id: int, app_id: int) -> list[Application]:
    """
    Takes a revision, inputs the current snapshot id into get_all_revisions_of_application
    to get all sibling revisions of the same application.
    
    Parameters:
        session (Session): SQLAlchemy session object.
        form_id (int): The ID of the form to which the application belongs.
        app_id (int): The ID of the revision to retrieve the sibling revisions for.
    
    Returns:
        list[Application]: A list of all "Application" instances that are sibling revisions of the specified application.
    """
    
    
    revision = get_application_by_id(session, form_id, app_id) # check if application exists
    
    applications = get_all_revisions_of_application(session, form_id, revision.snapshots.currentSnapshotID)
        
    return applications

def get_all_applications_of_type(session: Session, form_id: int) -> list[Application]:
    """
    Takes:\n
    A session\n
    A "form_id", specifying of which form to retrieve all appliations\n

    Returns:\n
    A list of all "Application" instances of the form which's id was given
    """
    applicationTable = get_application_table_by_id(form_id)
    applications: list[Application] = []
    
            

    allRows = dbActions.getRows(session, applicationTable)
    for row in allRows:
        if check_if_outdated(row.snapshots):
            continue
        applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    
    return applications


def get_all_applications(session: Session) -> list[Application]:
    """
    Returns all applications across all forms. Should be rejected by the API if the requesting user does not have admin/reporting privileges.
    
    Args:
        session (Session): SQLAlchemy session object.
    
    Returns:
        list[Application]: A list of all "Application" instances across all forms.
    """
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applications_of_type = get_all_applications_of_type(session, form.id)
        applications.extend(applications_of_type)

    return applications

def get_global_revisions(session: Session) -> list[Application]:
    """
    Returns all global revisions across all forms. Should be rejected by the API if the requesting user does not have admin/reporting privileges.
    
    Args:
        session (Session): SQLAlchemy session object.
    
    Returns:
        list[Application]: A list of all "Application" instances across all forms which are global revisions (nextSnapshotID != null).
    """
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        global_revisions_of_type = get_all_global_revisions_of_type(session, form.id)
        applications.extend(global_revisions_of_type)

    return applications


def get_applications_all_by_status(session: Session, status: str) -> list[Application]:
    """
    Returns all applications with a specific status across all forms.

    Args:
        session (Session): SQLAlchemy session object.
        status (str): The status to filter applications by. Must be one of "PENDING", "APPROVED", "REJECTED", or "REVISED".

    Raises:
        ValueError: If the status is invalid.

    Returns:
        list[Application]: A list of all "Application" instances with the specified status.
    """
    if status not in ["PENDING", "APPROVED", "REJECTED", "REVISED"]:
        raise ValueError("Invalid status")
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applicationTable = get_application_table_by_id(form.id)
        rows = getRowsByFilter(session, applicationTable, {"status": status})
        for row in rows:
            if check_if_outdated(row.snapshots):
                continue
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    return applications

def get_applications_public_by_status(session: Session, status: str) -> list[Application]:
    """
    Returns all applications with a specific status across all forms.

    Args:
        session (Session): SQLAlchemy session object.
        status (str): The status to filter applications by. Must be one of "PENDING", "APPROVED", "REJECTED", or "REVISED".

    Raises:
        ValueError: If the status is invalid.

    Returns:
        list[Application]: A list of all "Application" instances with the specified status.
    """
    if status not in ["PENDING", "APPROVED", "REJECTED", "REVISED"]:
        raise ValueError("Invalid status")
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applicationTable = get_application_table_by_id(form.id)
        rows = getRowsByFilter(session, applicationTable, {"status": status, "is_public": True})
        for row in rows:
            if check_if_outdated(row.snapshots):
                continue
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    return applications

def get_applications_private_by_status(session: Session, status: str) -> list[Application]:
    """
    Returns all applications with a specific status across all forms.

    Args:
        session (Session): SQLAlchemy session object.
        status (str): The status to filter applications by. Must be one of "PENDING", "APPROVED", "REJECTED", or "REVISED".

    Raises:
        ValueError: If the status is invalid.

    Returns:
        list[Application]: A list of all "Application" instances with the specified status.
    """
    if status not in ["PENDING", "APPROVED", "REJECTED", "REVISED"]:
        raise ValueError("Invalid status")
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applicationTable = get_application_table_by_id(form.id)
        rows = getRowsByFilter(session, applicationTable, {"status": status, "is_public": False})
        for row in rows:
            if check_if_outdated(row.snapshots):
                continue
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    return applications


def get_applications_by_user_id(session: Session, user_id: int) -> list[Application]:
    """
    Returns all applications submitted by a specific user across all forms.
    Should be rejected by the API if the requesting user does not match the user_id or does not have admin/reporting privileges.
    
    ARGS:
        session (Session): SQLAlchemy session object.
        user_id (int): The ID of the user whose applications are to be retrieved.
    
    RETURNS:
        list[Application]: List of Application objects submitted by the specified user.
    """
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applicationTable = get_application_table_by_id(form.id)
        rows = getRowsByFilter(session, applicationTable, {"user_id": user_id})
        for row in rows:
            if check_if_outdated(row.snapshots):
                continue
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    return applications

def get_applications_by_user_id_with_revisions(session: Session, user_id: int) -> list[Application]:
    """
    Returns all applications submitted by a specific user across all forms, including their revisions.
    Should be rejected by the API if the requesting user does not match the user_id or does not have admin/reporting privileges.
    
    ARGS:
        session (Session): SQLAlchemy session object.
        user_id (int): The ID of the user whose applications are to be retrieved.
    
    RETURNS:
        list[Application]: List of Application objects submitted by the specified user, including revisions.
    """
    applications: list[Application] = []
    all_forms = formCrud.get_all_forms(session)
    for form in all_forms:
        applicationTable = get_application_table_by_id(form.id)
        rows = getRowsByFilter(session, applicationTable, {"user_id": user_id})
        for row in rows:
            applications.append(rowToApplication(row=row, applicationTable=applicationTable))
    return applications

# def get_all_public_applications(session: Session) -> list[Application]:
#     """
#     Returns all applications that are marked as public.
    
#     ARGS:
#         session (Session): SQLAlchemy session object.
    
#     RETURNS:
#         list[Application]: List of public Application objects.
#     """
#     applications: list[Application] = []
#     all_forms = formCrud.get_all_forms(session)
#     for form in all_forms:
#         applications_of_type = get_all_applications_of_type(session, form.id)
#         applications.extend(applications_of_type)
#     public_applications : list[Application] = []
#     for application in applications:
#         if application.is_public:
#             public_applications.append(application)
#     return public_applications

# def get_all_private_applications(session: Session) -> list[Application]:
#     """
#     Returns all applications that are marked as public.
    
#     ARGS:
#         session (Session): SQLAlchemy session object.
    
#     RETURNS:
#         list[Application]: List of public Application objects.
#     """
#     applications: list[Application] = []
#     all_forms = formCrud.get_all_forms(session)
#     for form in all_forms:
#         applications_of_type = get_all_applications_of_type(session, form.id)
#         applications.extend(applications_of_type)
#     private_applications : list[Application] = []
#     for application in applications:
#         if not application.is_public:
#             private_applications.append(application)
#     return private_applications

# def old_insert_application(session:Session, application: Application):
#     """
#     Takes:\n
#     A session\n
#     An "Application" object\n
#     Does:\n
#     Inserts the application into the table of the form which's "form_id" the application contains\n\n

#     Returns:\n
#     The created instance of the application in the table, this is NOT an "Application" instance, but an instance of the applicationTable
#     """
#     applicationTable = get_application_table_by_id(id = application.form_id)
#     application_in_db = applicationTable(   
#         user_id =application.user_id,
#         form_id = application.form_id,
#         admin_id = application.admin_id,
#         status = application.status,
#         is_public = application.is_public,
#         created_at = application.created_at,
#         snapshots = application.snapshots.to_json()
#         )
#     for key in application.jsonPayload.keys():
#         setattr(application_in_db, application.jsonPayload[key]["label"] , application.jsonPayload[key]["value"])
#     created_app = dbActions.insertRow(session, applicationTable, application_in_db)
#     updated_app = dbActions.updateRow(session, applicationTable, {"id": created_app.id, "current_snapshot_id": created_app.id})
#     return updated_app

def insert_application(session: Session, application: Application):
    """
    Takes a session and an Application object, prepares the data,
    and inserts it into the correct dynamic form table.

    The application's own ID is set as its currentSnapshotID.

    Returns the created ORM instance from the database.
    """
    # 1. Prepare a clean data dictionary from the Pydantic model.
    # Exclude fields that are handled specially or aren't columns.
    app_data = application.model_dump(exclude={"id", "snapshots", "jsonPayload"})

    # 2. Unpack the jsonPayload into the main data dictionary.
    # This converts {"1": {"label": "email", "value": "a@b.com"}}
    # into {"email": "a@b.com"}.
    payload_fields = {
        item["label"]: item["value"]
        for item in application.jsonPayload.values()
    }
    app_data.update(payload_fields)
    
    # 3. Get the dynamic ORM table class for this form.
    applicationTable = get_application_table_by_id(id=application.form_id)

    # 4. Insert the row with a temporary snapshots value.
    # The `insertRow` function's `session.flush()` will assign an ID.
    app_data['snapshots'] = application.snapshots.to_json()
    created_app = dbActions.insertRow(session, applicationTable, app_data)

    return created_app

# wrapper for updating application status
def updateApplicationStatus(session: Session, form_id: int, app_id: int, newStatus: ApplicationStatus):
    if newStatus not in [ApplicationStatus.PENDING, ApplicationStatus.APPROVED, ApplicationStatus.REJECTED, ApplicationStatus.REVISED]:
        raise ValueError("Invalid status")
    tableClass = get_application_table_by_id(form_id)
    return dbActions.updateRow(session, tableClass, {"id": app_id, "status": newStatus})


def update_application(form_id: int, app_id: int, updateDict: dict, session: Session) -> int:
    """
    TODO 
    Returns:
        id of newly created updated application (int)
    """

    updated_app = get_application_by_id(session, form_id, app_id) # Get application to update
    
    # -- PREPARE NEW APPLICATION --
    updated_app.id = None  # Set id to None to create a new entry
    updated_app.snapshots.currentSnapshotID = -1
    updated_app.snapshots.previousSnapshotID = app_id
    updated_app.snapshots.nextSnapshotID = None
    
    # -- JSON --
    label_key_dict = {}

    for key, block in updated_app.jsonPayload.items():
        label_key_dict[block["label"]] = key

    for key, block in updateDict.items():
        if block["label"] in label_key_dict.keys():
            updated_app.jsonPayload[label_key_dict[block["label"]]] = block
            
    # -- INSERT NEW APPLICATION --
    new_orm_app = insert_application(session, updated_app)  # Insert updated application as new row
    # session.commit()
    # session.refresh(new_orm_app)
    new_app_id = new_orm_app.id
    
    # -- UPDATE ORIGINAL APPLICATION --
    applicationTable = dbActions.get_application_table_by_id(form_id)
    original_orm_app = dbActions.getRowById(session, applicationTable, app_id)
    
    if original_orm_app:
        snapshots_obj = Snapshots.from_json(original_orm_app.snapshots)
        snapshots_obj.nextSnapshotID = new_app_id
        snapshots_obj.currentSnapshotID = new_app_id # CHANGED: Mark original as outdated.
        original_orm_app.snapshots = snapshots_obj.to_json()
        session.commit()
    
    # -- UPDATE ALL OLD REVISIONS --
    old_revisions = get_all_revisions_of_application(session, form_id, app_id)
    for revision in old_revisions:
        if revision.id == app_id or revision.id == new_app_id:
            continue
        revision_orm_app = dbActions.getRowById(session, applicationTable, revision.id)
        if revision_orm_app:
            snapshots_obj = Snapshots.from_json(revision_orm_app.snapshots)
            snapshots_obj.currentSnapshotID = new_app_id # CHANGED: Mark old revisions as outdated.
            revision_orm_app.snapshots = snapshots_obj.to_json()
            session.commit()
    
    return new_app_id


# --- HELPER FUNCTIONS ---


## -- functions for snapshots -- ##

def _snapshot_to_dict(snapstring: str) -> dict:
    return json.loads(snapstring)

def check_if_outdated(snapstring: str) -> bool:
    """
    Takes an application, checks if it is outdated\n
    Returns True if outdated, False if up-to-date
    """
    snapshots = _snapshot_to_dict(snapstring)
    if snapshots["currentSnapshotID"] >= 0:
        return True
    return False

def get_current_snapshot_id(snapstring: str) -> int:
    """
    Takes an application, returns the currentSnapshotID
    """
    snapshots = _snapshot_to_dict(snapstring)
    return snapshots["currentSnapshotID"]
