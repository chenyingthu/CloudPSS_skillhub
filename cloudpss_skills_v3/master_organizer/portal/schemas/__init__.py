"""Data transfer objects for API requests and responses."""

from .common import BaseResponse, ErrorResponse, Pagination
from .case import CaseCreate, CaseUpdate, CaseResponse
from .task import TaskCreate, TaskUpdate, TaskResponse, TaskRunRequest
from .result import ResultResponse, ResultSummaryResponse

__all__ = [
    # Common
    "BaseResponse",
    "ErrorResponse",
    "Pagination",
    # Case
    "CaseCreate",
    "CaseUpdate",
    "CaseResponse",
    # Task
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskRunRequest",
    # Result
    "ResultResponse",
    "ResultSummaryResponse",
]
