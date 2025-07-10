from typing import Literal, Optional, TypedDict, Dict
from typing_extensions import NotRequired
from src.models.base import BaseResourceObject

class BaseProcEvent(TypedDict):
    action: str

class ProcessEvent(BaseProcEvent):
    processName: str
    data: Optional[Dict]

class LogEvent(BaseProcEvent):
    level: str
    message: str

class HttpEvent(BaseProcEvent):
    name: str
    data: BaseResourceObject

class DbEvent(BaseProcEvent):
    pass