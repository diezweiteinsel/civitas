from dataclasses import dataclass
from datetime import date
from backend.models import UserType, User
from backend.core import db
from backend.models.domain.user import RoleAssignment

@dataclass
class SimpleUser:
    id: int | None
    name: str
    email: str


"""function that assigns roles to users. Raises an error if the user already has the role. Users can have multiple roles."""
def assign_role(user: User, role: UserType) -> None:
    if any(r.role == role for r in user.user_roles):
        raise ValueError(f"User already has role {role}")
    user.user_roles.append(RoleAssignment(
        user_id=user.id,
        role=role,
        assignment_date=date.today()
    ))

"""Ensure the user is an admin; raise PermissionError if not."""
def ensure_admin(user: User) -> bool:
	if not user or any(r.role == UserType.ADMIN for r in user.user_roles) < 1: 
		return False
	return True

"""Ensure the user is an applicant; raise PermissionError if not."""
def ensure_applicant(user: User) -> bool:
	if not user or any(r.role == UserType.APPLICANT for r in user.user_roles) < 1: 
		return False
	return True

"""Ensure the user is a reporter; raise PermissionError if not."""
def ensure_reporter(user: User) -> bool:
	if not user or any(r.role == UserType.REPORTER for r in user.user_roles) < 1: 
		return False
	return True


class UserLogic:
    """Business logic related to User operations.

    This class provides a few helper methods and also acts as a namespace
    for DB helpers used by the tests.
    """

    def __init__(self, user: User):
        self.user = user

    def display(self):
        return f"User(id={self.user.id}, name={self.user.username}, email={self.user.email})"

    @classmethod
    def get_user_by_id(cls, user_id: int) -> SimpleUser | None:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
                row = cur.fetchone()
                if row:
                    return SimpleUser(id=row[0], name=row[1], email=row[2])
                return None

    @classmethod
    def get_user_by_email(cls, email: str) -> SimpleUser | None:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    return SimpleUser(id=row[0], name=row[1], email=row[2])
                return None


# ---- Database interactions used by tests ----

def create_table():
    """Create the users table used by the tests.

    The tests expect columns: id, name, email
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id serial PRIMARY KEY,
                    name varchar NOT NULL,
                    user_type varchar NOT NULL,
                    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    email varchar UNIQUE
                )
            """)
            conn.commit()


def add_user(name: str, user_type: UserType) -> User:
    with db.get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute("INSERT INTO users (name, user_type) VALUES (%s, %s) RETURNING id",
                        (name, user_type.value))
            row = cur.fetchone()
            conn.commit()
            return User(id=row[0],
                        username=name,
                        user_type=user_type,
                        date_created=datetime.now())

def add_user_email(user_id: int, email: str) -> None:
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))
            conn.commit()

def get_all_users() -> list[User]:
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, user_type, date_created FROM users ORDER BY id")
            rows = cur.fetchall()
            return [User(id=r[0],
                         username=r[1],
                         email=r[2],
                         user_type=r[3],
                         date_created=r[4]) for r in rows]


def delete_user(user_id: int) -> None:
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()


if __name__ == "__main__":
    # quick smoke-run
    create_table()
    u = add_user("alice", "APPLICANT")
    print(get_all_users())
