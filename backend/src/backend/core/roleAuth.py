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
    user_role_assignments =  roletable.get_user_roles_by_id(user_id=user_id, session=session)
    for role_assignment in user_role_assignments:
        if role_assignment.role == role:
            return True
    return False