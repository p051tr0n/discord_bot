from typing import (
    Dict,
    List,
    Optional,
    Union,
    Any,
    Tuple,
    TypedDict,
    TYPE_CHECKING,
    Literal
)

from src.obj_types.resource_types.snowflake import Snowflake

class GatewayEvent(TypedDict):
    op: int
    d: Optional[Dict]
    s: Optional[int]
    t: Optional[str]

class AutoModActionObject(TypedDict):
    type: str
    metadata: Dict[str, Any]

class AutoModRuleObject(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    name: str
    creator_id: Snowflake
    event_type: str
    trigger_type: str
    trigger_metadata: Dict[str, Any]
    actions: List[AutoModActionObject]
    enabled: bool
    exempt_roles: List[Snowflake]
    exempt_channels: List[Snowflake]

class Presence(TypedDict):
    since: Optional[int]
    status: Optional[str]
    activities: Optional[List[Dict[str, Any]]]
    afk: Optional[bool]

class Hello(GatewayEvent):
    heartbeat_interval: int

class Ready(GatewayEvent):
    v: int
    user: Dict[str, Any]
    guilds: List[Dict[str, Any]]
    session_id: str
    shard: List[int]
    application: Dict[str, Any]

class Resumed(GatewayEvent):
    pass

class Reconnect(GatewayEvent):
    pass

class InvalidSession(GatewayEvent):
    resumable: bool


class ConnectionProperties(TypedDict):
    os: str
    browser: str
    device: str

class IdentifyEvent(GatewayEvent):
    token: str
    intents: int
    properties: ConnectionProperties
    compress: Optional[bool]
    large_threshold: Optional[int]
    shard: Optional[List[int]]
    presence: Optional[Presence]
    heartbeat_interval: Optional[int]

class ResumeEvent(GatewayEvent):
    token: str
    session_id: str
    seq: int

class HeartbeatEvent(GatewayEvent):
    seq: int

class RequestGuildMembersEvent(GatewayEvent):
    guild_id: Snowflake
    query: Optional[str]
    limit: int
    presences: Optional[bool]
    user_ids: Optional[List[Snowflake]]
    nonce: Optional[str]