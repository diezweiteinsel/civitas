

def test_get_current_user_payload_invalid_token():
    from backend.api.deps import get_current_user_payload
    from fastapi import HTTPException
    import pytest
    from jose import jwt

    # Test with an invalid token
    invalid_token = "this.is.an.invalid.token"
    with pytest.raises(HTTPException) as exc_info:
        import asyncio
        asyncio.run(get_current_user_payload(token=invalid_token))
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

def test_get_current_user_payload_valid_token():
    from backend.api.deps import get_current_user_payload
    from backend.core.security import SECRET_KEY, ALGORITHM
    from jose import jwt
    import asyncio

    # Create a valid token for testing
    test_payload = {
        "sub": "42",
        "username": "testuser",
        "roles": ["admin", "user"],
        "exp": 9999999999  # far future expiration for testing
    }
    valid_token = jwt.encode(test_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Test with the valid token
    payload = asyncio.run(get_current_user_payload(token=valid_token))
    assert payload["sub"] == "42"
    assert payload["username"] == "testuser"
    assert payload["roles"] == ["admin", "user"]
    
    
    def test_get_current_user_payload_expired_token():
        from backend.api.deps import get_current_user_payload
        from backend.core.security import SECRET_KEY, ALGORITHM
        from jose import jwt
        import asyncio
        from fastapi import HTTPException
        import pytest
        import time

        # Create an expired token for testing
        test_payload = {
            "sub": "42",
            "username": "testuser",
            "roles": ["admin", "user"],
            "exp": int(time.time()) - 10  # expired 10 seconds ago
        }
        expired_token = jwt.encode(test_payload, SECRET_KEY, algorithm=ALGORITHM)

        # Test with the expired token
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(get_current_user_payload(token=expired_token))
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"

def test_get_current_user_payload_wrong_signature_token():
    from backend.api.deps import get_current_user_payload
    from backend.core.security import ALGORITHM
    from jose import jwt
    import asyncio
    from fastapi import HTTPException
    import pytest

    # Create a token with a wrong signature for testing
    test_payload = {
        "sub": "42",
        "username": "testuser",
        "roles": ["admin", "user"],
        "exp": 9999999999  # far future expiration for testing
    }
    wrong_signature_token = jwt.encode(test_payload, "IamWrong", algorithm=ALGORITHM)

    # Test with the token that has a wrong signature
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_current_user_payload(token=wrong_signature_token))
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

def test_role_checker():
    from backend.api.deps import RoleChecker
    from fastapi import HTTPException
    import pytest
    import asyncio

    async def mock_payload_admin():
        return {"roles": ["admin", "user"]}

    async def mock_payload_user():
        return {"roles": ["user"]}

    async def mock_payload_no_roles():
        return {"roles": []}

    role_checker_admin = RoleChecker(allowed_roles=["admin"])

    # resolve async mocks to plain dicts
    payload_admin = asyncio.run(mock_payload_admin())
    payload_user = asyncio.run(mock_payload_user())
    payload_no_roles = asyncio.run(mock_payload_no_roles())

    # Should pass for admin role (no asyncio.run on the checker)
    role_checker_admin(payload=payload_admin)

    # Should raise HTTPException for user role only
    with pytest.raises(HTTPException) as exc_info:
        role_checker_admin(payload=payload_user)
    assert exc_info.value.status_code == 403

    # Should raise HTTPException for no roles
    with pytest.raises(HTTPException) as exc_info:
        role_checker_admin(payload=payload_no_roles)
    assert exc_info.value.status_code == 403

    # Test RoleChecker with allowed role "user"
    role_checker_user = RoleChecker(allowed_roles=["user"])

    # Should pass for user role
    role_checker_user(payload=payload_user)

    # Should pass for admin role (since admin also has user role)
    role_checker_user(payload=payload_admin)

    # Should raise HTTPException for no roles
    with pytest.raises(HTTPException) as exc_info:
        role_checker_user(payload=payload_no_roles)
    assert exc_info.value.status_code == 403