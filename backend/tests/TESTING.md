# Tests for Civitas backend

Make sure to recreate the file structure of `civitas/backend/src/`, so we ensure that imports work correctly and we test all relevant parts of the codebase.

We test with `pytest` and `testcontainers` to spin up a temporary PostgreSQL database for testing purposes. This means, you need to have Docker installed **and running** on your machine.



> [!WARNING] Docker
> Once again, just to reiterate,
> **Make Sure Your Docker IS INSTALLED AND RUNNING!**

## How to do this in pytest

1. Install pytest if you haven't already, either through requirements.txt or manually:


```bash
pip install pytest
```

2. Create a test file, e.g., `test_api.py`, in the `civitas/backend/tests/` directory.

3. Make sure you replicate the directory structure of `civitas/backend/src/` within the tests directory, so ideally each module has a corresponding test file.
The structure should look something like this:

```bash
civitas/backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       └── user.py
├── tests/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       └── test_user.py
```

4. In each test file, import the necessary modules and write your test cases. For example, in `test_user.py`, you might have:

```python
import pytest
from src.api.endpoints.user import User # make sure you import from src to match the structure

@pytest.fixture
def user():
    return User()

def test_user_creation(user):
    assert user is not None
    assert user.id is not None
    # and so on...
```

5. Run your tests using pytest from the `civitas/backend/src/` directory individually or all at once. Navigate to `src` and set the `PYTHONPATH` to the current directory to ensure imports work correctly:

**Individually**:

```bash
pytest civitas/backend/tests/api/endpoints/test_user.py
```

**All at once**:

```bash
pytest
```

6. Review the test results in the terminal to see if all tests passed or if any failed.

> **Pytest** will now start the test and tell you if tests passed or failed. The very last line should say something like:
> `===== 6 passed, 6 warnings, 4 skipped in 3.81s ===`

You can now scroll up in the terminal to see which tests passed or failed and why.

7. If you need to debug a failing test, you can use `print` statements or a debugger to inspect the state of your application at various points.


This is clearly a #TODO.

