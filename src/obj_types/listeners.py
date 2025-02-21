from typing import Dict, List, Optional, TypedDict, Union, Any
from .events import GatewayEvent

class ListenerFilter(TypedDict):
    condition: str
    fields: Dict[str, Any]

class ListenerAction(TypedDict):
    type: str
    data: Dict[str, Any]

class ListenerObject(TypedDict):
    type: str
    filter: List[ListenerFilter]
    action: List[ListenerAction]