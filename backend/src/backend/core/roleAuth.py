from backend.models.orm import roletable



from sqlalchemy.orm import Session







def check_role(session: Session, user_id: int, role: str)-> bool:
    """
    Args:
        session(Session):
        user_id(int): id of user whose role to check
        role(str): "ADMIN", "APPLICANT" or "REPORTER" 
    Returns:
        True or False based on whether or not the user has the specified role.
    """
    orm_role_assignments =  roletable.get_user_roles_by_id(user_id=user_id, session=session)
    domain_role_assignments = []
    for orm_role_assignment in orm_role_assignments:
        domain_role_assignments.append(roletable.to_domain_model(orm_role_assignment))
    if domain_role_assignments == []:
        Exception("No role assignments found")
    for role_assignment in domain_role_assignments:
        print(role_assignment)
        print(role)
        if role_assignment:
            return True
    return False

