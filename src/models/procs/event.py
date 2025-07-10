from src.models.base import Base, BaseResourceObject

__all__ = ['ProcessEvent', 'LogEvent', 'HttpEvent']

class BaseProcEvent(Base):
    __slots__ = ('action')
    def __init__(self, **kwargs):
        self.action: str = kwargs.get('action', "")

class ProcessEvent(BaseProcEvent):
    __slots__ = ('processName', 'data')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data: str = kwargs.get('data', None)
        self.processName: str = kwargs.get('processName', "")

class LogEvent(BaseProcEvent):
    __slots__ = ('level', 'message')
    def __init__(self, level = "DEBUG", message = "", **kwargs):
        super().__init__(**kwargs)
        self.level: str = level
        self.message: str = message

class HttpEvent(BaseProcEvent):
    '''
        Name is the GatewayEvent type.
        Data is the resource object that represents the payload of the Gateway Event.
    '''
    __slots__ = ('name', 'data')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = kwargs.get('name', "")
        self.data: BaseResourceObject = kwargs.get('data')