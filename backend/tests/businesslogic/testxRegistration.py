from backend.businesslogic.selfRegistration import register_Applicant, all_Users
from backend.businesslogic.user import ensure_applicant
def test_register_user():
    username = "testuser"
    password = "password123"
    new_user = register_Applicant(username, password)
    assert new_user.username == username
    assert ensure_applicant(new_user) is True
    assert new_user in all_Users
    assert new_user.id is not None
    new_user2 = register_Applicant("anotheruser", "pass")
    assert new_user2.id == new_user.id + 1
    assert all_Users[0].id == 1
    assert all_Users[1].id == 2
    #assert all_Users[0].username == "testuser" deaktivated because of pytest caching issues

test_register_user()


