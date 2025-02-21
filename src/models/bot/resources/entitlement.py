from typing import List
from typing_extensions import Optional

from obj_types.resource_types.snowflake import Snowflake
from models.base import BaseResourceObject

__all__ = ['Entitlement']

class Entitlement(BaseResourceObject):
    __slots__ = (
        'id',
        'sku_id',
        'application_id',
        'user_id',
        'type',
        'deleted',
        'starts_at',
        'ends_at',
        'guild_id',
        'consumed'
    )

    def __init__(self, **kwargs):
        self.id: Snowflake                  = kwargs.get('id')
        self.sku_id: Snowflake              = kwargs.get('sku_id')
        self.application_id: Snowflake      = kwargs.get('application_id')
        self.user_id: Snowflake             = kwargs.get('user_id', None)
        self.type: int                      = kwargs.get('type', 0)
        self.deleted: bool                  = kwargs.get('deleted', False)
        self.starts_at: Optional[str]       = kwargs.get('starts_at', None)
        self.ends_at: Optional[str]         = kwargs.get('ends_at', None)
        self.guild_id: Optional[Snowflake]  = kwargs.get('guild_id', None)
        self.consumed: bool                 = kwargs.get('consumed', None)