# standard library imports
from datetime import date, datetime

# third party imports
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# project imports
from backend.core.security import hash_password
from backend.core import db
from backend.models import User, UserType
from backend.crud import userCrud
from backend.models.domain.user import RoleAssignment, UserCreatePayload, UserID

router = APIRouter(prefix="/users", tags=["users"])

#TODO: implement following endpoints:
# - GET users/me
# - PUT users/me
# - GET users/ (list all users) - DONE, but needs fixing: no returning of hashed_password
# - POST users/ (create new user) - DONE
# - GET users/{user_id}
# - PUT users/{user_id}
# - DELETE users/{user_id}

# ALL THESE need proper logic still and need to be wired to the database


@router.get("/me", response_model=User, tags=["Users"], summary="Get current user")
async def get_current_user():
    """
    Retrieve the currently authenticated user.
    """
    return User(id=1, username="alice", user_type=UserType.APPLICANT, date_created=datetime(2023, 10, 1, 12, 0, 0))

@router.put("/me", response_model=User, tags=["Users"], summary="Update current user")
async def update_current_user(user: User):
    """
    Update the currently authenticated user's information.
    """
    user.id = 1  # Simulate current user ID
    return user



@router.get("", response_model=list[User], tags=["Users"], summary="List all users")
async def list_users():
    """
    Retrieve all users in the system.
    """
    try:
        with db.get_session() as session:
            users = userCrud.get_all_users(session)
            return users
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return []

    # this gets already serialized, we receive the data from the model? from sqlalchemy from the DB
    # REST API <-- [main (controller)] <-- [api] <-- [routers] <-- [user routers] <-- [models] <-- [database (ORM)]

@router.post("",
            response_model=UserID,
            status_code=status.HTTP_201_CREATED,
            tags=["Users"],
            summary="Create a new user")

async def create_user(userjson: UserCreatePayload, session: Session = Depends(db.get_session_dep)):
    """
    Create a new user in the system.
    """
    # 1 CHECK IF USERNAME OR EMAIL ALREADY EXISTS
    db_user = userCrud.get_user_by_name(userjson.username, session)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    db_usermail = userCrud.get_user_by_email(userjson.email, session)
    if db_usermail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(userjson.password)
    # 2 PREPARE USER OBJECT
    new_user = User(
        username=userjson.username,
        email=userjson.email,
        hashed_password=hashed_password,
        date_created=date.today()
    )

    # 2b ASSIGN ROLE TO USER
    assigned_role = RoleAssignment(
        role = userjson.role,
        assignment_date = date.today()
    )


    new_user.user_roles.append(assigned_role)


    # 1) Validate and process the user data
    # 2) Hand over session using dependency injection
    # 3) Call the CRUD function to add the user to the database
    orm_user = userCrud.add_user(session, new_user)
    if not orm_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user."
        )
    return UserID(id=orm_user.id)


@router.get("/{user_id}", response_model=User, tags=["Users"], summary="Get user by ID")
async def get_user(user_id: int):
    """
    Retrieve a user by their ID.
    """
    try:
        with db.get_session() as session:
            user = userCrud.get_user_by_id(user_id, session)
            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        print(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{user_id}", response_model=User, tags=["Users"], summary="Update user by ID")
async def update_user(user_id: int, user: User):
    """
    Update an existing user's information.
    """
    user.id = user_id
    return user

@router.delete("/{user_id}", tags=["Users"], summary="Delete user by ID")
async def delete_user(user_id: int):
    """
    Delete a user from the system.
    """
    return {"message": f"User {user_id} deleted"}



