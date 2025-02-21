import config
from enum import Enum
from models.base import Base

TRIGGER_FIELD_LIMITS = {
    "keyword_filter": {
        "max_array_length": 1000,
        "max_char_per_string": 60,
        "trigger_types": [AutoModTrigger.KEYWORD.value, AutoModTrigger.KEYWORD_PRESET.value]
    },
    "action_type":{
        1: "BLOCK_MESSAGE",
        2: "SEND_ALERT_MESSAGE",
        3: "TIMEOUT",
        4: "BLOCK_MEMBER_INTERACTION"
    },
    "action_metadata":
    {
        "SEND_ALERT_MESSAGE": {
            "field": "channel_id",
            "type": "snowflake",
            "constraints": "channel must exist"
        },
        "TIMEOUT": {
            "field": "duration_seconds",
            "type": "integer",
            "constraints": "maximum of 2419200 seconds (28 days)"
        },
        "BLOCK_MESSAGE": {
            "field": "custome_message",
            "type": "string",
            "constraints": "maximum of 150 characters"
        }
    }
}

class AutoModTrigger(Enum):
    KEYWORD = 1
    SPAM = 3
    KEYWORD_PRESET = 4
    MENTION_SPAM = 5
    MEMBER_PROFILE = 6

class AutoModKeywordPreset(Enum):
    PROFANITY = 1
    SEXUAL_CONTENT = 2
    SLURS = 3

class AutoModActionObject(Base):

    def __init__(self, **kwargs):
        '''
            Represents the Auto Mod Action Object Structure defined here: https://discord.com/developers/docs/resources/guild#unavailable-guild-object
        '''
        super().__init__(**kwargs)
        self.type = kwargs.pop('type', '')
        self.metadata = dict()

        self.setMetadata(kwargs.pop('metadata'))

    def setMetadata(self, metadata):
        if self.type == 'BLOCK_MESSAGE':
            self.metadata = {
                "custom_message": metadata.get('custom_message', '')
            }
        elif self.type == 'SEND_ALERT_MESSAGE':
            self.metadata = {
                "channel_id": metadata.get('channel_id', '')
            }
        elif self.type == 'TIMEOUT':
            self.metadata = {
                "duration_seconds": metadata.get('duration_seconds', 0)
            }
        else:
            self.metadata = dict()


class AutoModRuleObject(Base):

    def __init__(self, **kwargs):
        '''
            Represents the Auto Mod Object Structure defined here: https://discord.com/developers/docs/resources/guild#unavailable-guild-object
        '''
        super().__init__(**kwargs)
        self.id = kwargs.pop('id', '')
        self.guild_id = kwargs.pop('guild_id', '')
        self.name = kwargs.pop('name', '')
        self.creator_id = kwargs.pop('creator_id', '')
        self.event_type = kwargs.pop('event_type', '')
        self.trigger_type = kwargs.pop('trigger_type', '')
        self.trigger_metadata = kwargs.pop('trigger_metadata', dict())
        self.actions = kwargs.pop('actions', list())
        self.enabled = kwargs.pop('enabled', False)
        self.exempt_roles = kwargs.pop('exempt_roles', list())
        self.exempt_channels = kwargs.pop('exempt_channels', list())