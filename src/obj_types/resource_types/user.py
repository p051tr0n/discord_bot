from typing import Literal, Optional, TypedDict
from typing_extensions import NotRequired

from .snowflake import Snowflake

class UserAvatarDecoration(TypedDict):
    asset: str
    sku_id: Snowflake

class PartialUser(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    global_name: Optional[str]
    avatar_decoration_data: NotRequired[UserAvatarDecoration]

class User(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    global_name: Optional[str]
    bot: NotRequired[bool]
    system: NotRequired[bool]
    mfa_enabled: NotRequired[bool]
    locale: NotRequired[str]
    verified: NotRequired[bool]
    email: NotRequired[str]
    flags: NotRequired[int]
    premium_type: NotRequired[Literal[0, 1, 2]]
    public_flags: NotRequired[int]
    avatar_decoration_data: NotRequired[UserAvatarDecoration]

