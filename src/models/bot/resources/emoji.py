from src.models.base import BaseResourceObject

__all__ = ['Emoji']

class Emoji(BaseResourceObject):
    __slots__ = ('id', 'name', 'roles', 'user', 'require_colons', 'managed', 'animated', 'available')
    def __init__(self, **kwargs):
        self.id                 = kwargs.get('id', "")
        self.name               = kwargs.get('name', "")
        self.roles              = kwargs.get('roles', None)
        self.user               = kwargs.get('user', None)
        self.require_colons     = kwargs.get('require_colons', None)
        self.managed            = kwargs.get('managed', None)
        self.animated           = kwargs.get('animated', None)
        self.available          = kwargs.get('available', None)