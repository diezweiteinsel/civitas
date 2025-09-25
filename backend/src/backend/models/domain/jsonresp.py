from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class JsonResponse:
    success: bool
    message: str
    data: Optional[Any] = None

@dataclass
class PaginatedResponse:
    success: bool
    message: str
    data: List[Any]
    total: int
    page: int
    page_size: int