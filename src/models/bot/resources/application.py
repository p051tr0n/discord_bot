from models.base import BaseResourceObject
from obj_types.resource_types.snowflake import Snowflake

class PartialApplication(BaseResourceObject):
    __slots__ = ('id', 'flags')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: Snowflake = kwargs.pop('id', '')
        self.flags: int = kwargs.pop('flags', 0)