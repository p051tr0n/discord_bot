from src.models.base import Base

class Presence(Base):

    def __init__(self, **kwargs):
        '''
            Represents the Presence Structure defined here: https://discord.com/developers/docs/events/gateway-events#update-presence

            since: int
                Unix time (in milliseconds) of when the client went idle, or null if the client is not idle.

            activities: list
                The user's activities.

            status: str
                The user's new status.

            afk: bool
                Whether or not the client is afk.
        '''
        if not self.checkStatus(kwargs['status']):
            #TODO: Log this error object
            objs = {k: v for k, v in kwargs.items()}
            errLogMsg = self._create_error_message('Invalid Presence.', objs)
            raise ValueError('Invalid status value.')
        
        self.since = kwargs.pop('since', None)
        self.activities = kwargs.pop('activities', None)
        self.status = kwargs.pop('status', None)
        self.afk = kwargs.pop('afk', False)

    #-------------------------------------------------------------------------------
    def checkStatus(self, status: str) -> bool:
        '''
            Check if the status is valid.
        '''
        return status in ['online', 'dnd', 'idle', 'invisible', 'offline']
        