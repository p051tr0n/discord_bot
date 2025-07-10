from typing import List, Optional
from src.models.base import BaseResourceObject
from src.obj_types.resource_types.snowflake import Snowflake


__all__ = ['AutoModerationRule',
            'AutoModerationAction', 
            'AutoModerationActionMetadata', 
            'AutoModerationTriggerMetadata', 
            'AutoModerationActionExecution']

class AutoModerationActionMetadata(BaseResourceObject):
    __slots__ = ('channel_id', 'duration_seconds', 'custom_message')

    def __init__(self, **kwargs):
        self.channel_id: Snowflake          = kwargs.get('channel_id')
        self.duration_seconds: int          = kwargs.get('duration_seconds')
        self.custom_message: Optional[str]  = kwargs.get('custom_message', None)

#-------------------------------------------------------------------------------------------
class AutoModerationAction(BaseResourceObject):
    __slots__ = ('type', 'metadata')
    def __init__(self, **kwargs):
        self.type: int = kwargs.get('type')
        self.metadata: Optional[AutoModerationActionMetadata] = AutoModerationActionMetadata(**kwargs.get('metadata', {})) if 'metadata' in kwargs and kwargs['metadata'] is not None else None

#-------------------------------------------------------------------------------------------
class AutoModerationTriggerMetadata(BaseResourceObject):
    __slots__ = ('keyword_filter', 
                'regex_patterns',
                'presets',
                'allow_list',
                'mention_total_limit',
                'metion__raid_protection_enabled')

    def __init__(self, **kwargs):
        self.keyword_filter: List[str]              = kwargs.get('keyword_filter', False)
        self.regex_patterns: List[str]              = kwargs.get('regex_patterns', [])
        self.presets: List[int]                     = kwargs.get('presets', [])
        self.allow_list: List[str]                  = kwargs.get('allow_list', [])
        self.mention_total_limit: int               = kwargs.get('mention_total_limit', 0)
        self.metion__raid_protection_enabled: bool  = kwargs.get('metion__raid_protection_enabled', False)

#-------------------------------------------------------------------------------------------
class AutoModerationRule(BaseResourceObject):

    __slots__ = ('id',
                'guild_id',
                'name',
                'creator_id',
                'event_type',
                'trigger_type',
                'trigger_metadata',
                'actions',
                'enabled',
                'exempt_roles',
                'exempt_channels')
    
    def __init__(self, **kwargs):
        self.id: Snowflake                                      = kwargs.get('id', "")
        self.guild_id: Snowflake                                = kwargs.get('guild_id', "")
        self.name: str                                          = kwargs.get('name', "")
        self.creator_id: Snowflake                              = kwargs.get('creator_id', "")
        self.event_type: int                                    = kwargs.get('event_type', "")
        self.trigger_type: int                                  = kwargs.get('trigger_type', "")
        self.trigger_metadata: AutoModerationTriggerMetadata    = AutoModerationTriggerMetadata(**kwargs.get('trigger_metadata')) if 'trigger_metadata' in kwargs and kwargs['trigger_metadata'] is not None else AutoModerationTriggerMetadata()
        self.actions: List[AutoModerationAction]                = [AutoModerationAction(**x) for x in kwargs.get('actions')] if 'actions' in kwargs and kwargs['actions'] is not None else []
        self.enabled: bool                                      = kwargs.get('enabled', False)
        self.exempt_roles: List[Snowflake]                      = kwargs.get('exempt_roles', [])
        self.exempt_channels: List[Snowflake]                   = kwargs.get('exempt_channels', [])

#-------------------------------------------------------------------------------------------
class AutoModerationActionExecution(BaseResourceObject):
    __slots__ = ('guild_id',
                'action',
                'rule_id',
                'rule_trigger_type',
                'user_id',
                'channel_id',
                'message_id',
                'alert_system_message_id',
                'content',
                'matched_keyword',
                'matched_content')
    
    def __init__(self, **kwargs):
        self.guild_id: Snowflake                            = kwargs.get('guild_id', "")
        self.action: AutoModerationAction                   = AutoModerationAction(**kwargs.get('action'))
        self.rule_id: Snowflake                             = kwargs.get('rule_id', "")
        self.rule_trigger_type: int                         = kwargs.get('rule_trigger_type', "")
        self.user_id: Snowflake                             = kwargs.get('user_id', "")
        self.channel_id: Optional[Snowflake]                = kwargs.get('channel_id', "")
        self.message_id: Optional[Snowflake]                = kwargs.get('message_id', "")
        self.alert_system_message_id: Optional[Snowflake]   = kwargs.get('alert_system_message_id', "")
        self.content: str                                   = kwargs.get('content', None)
        self.matched_keyword: str                           = kwargs.get('matched_keyword', "")
        self.matched_content: str                           = kwargs.get('matched_content', None)