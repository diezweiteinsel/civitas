"""Compatibility shim: expose domain user types as `backend.models.user`.

Some modules import `backend.models.user` directly. The real implementation lives
in `backend.models.domain.user`. This file re-exports the main symbols so both
import styles work (installed package and local imports).
"""

from .domain.user import Account, AccountStatus, User, UserType

__all__ = ["User", "UserType", "AccountStatus", "Account"]
