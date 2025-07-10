from typing import List
from typing_extensions import Optional
from src.models.base import BaseResourceObject

__all__ = ['AuditLogChange', 'OptionalAuditLogEntry', 'AuditLogEntry']

#-----------------------------------------------------------------------------------------------------------------
class AuditLogChange(BaseResourceObject):
    __slots__ = (
                    'key',
                    'old_value',
                    'new_value'
                )
    
    def __init__(self, **kwargs):
        self.key: str       = kwargs.get('key')
        self.old_value      = kwargs.get('old_value', None)
        self.new_value      = kwargs.get('new_value', None)

#-----------------------------------------------------------------------------------------------------------------
class OptionalAuditLogEntry(BaseResourceObject):
    __slots__ = (
                    'application_id',
                    'auto_moderation_rule_name',
                    'auto_moderation_rule_trigger_type',
                    'channel_id',
                    'count',
                    'delete_member_days',
                    'id',
                    'members_removed',
                    'message_id',
                    'role_name',
                    'type',
                    'integration_type'
                )
    def __init__(self, **kwargs):
        self.application_id: str                = kwargs.get('application_id')
        self.auto_moderation_rule_name: str     = kwargs.get('auto_moderation_rule_name')
        self.auto_moderation_rule_trigger_type  = kwargs.get('auto_moderation_rule_trigger_type')
        self.channel_id: str                    = kwargs.get('channel_id')
        self.count: int                         = kwargs.get('count')
        self.delete_member_days: str            = kwargs.get('delete_member_days')
        self.id: str                            = kwargs.get('id')
        self.members_removed: str               = kwargs.get('members_removed')
        self.message_id: str                    = kwargs.get('message_id')
        self.role_name: str                     = kwargs.get('role_name')
        self.type: int                          = kwargs.get('type')
        self.integration_type: str              = kwargs.get('integration_type')

#-----------------------------------------------------------------------------------------------------------------
class AuditLogEntry(BaseResourceObject):
    __slots__ = (
                    'target_id',
                    'changes',
                    'user_id',
                    'id',
                    'action_type',
                    'options',
                    'reason'
                )
    
    def __init__(self, **kwargs):
        self.target_id: str                             = kwargs.get('target_id')
        self.changes: Optional[List[AuditLogChange]]   = [AuditLogChange(**x) for x in kwargs.get('changes')] if 'changes' in kwargs and kwargs['changes'] is not None else None
        self.user_id: str                               = kwargs.get('user_id')
        self.id: str                                    = kwargs.get('id')
        self.action_type: int                           = kwargs.get('action_type')
        self.options: Optional[AuditLogEntry]           = OptionalAuditLogEntry(**kwargs.get('options')) if 'options' in kwargs and kwargs['options'] is not None else None
        self.reason: Optional[str]                     = kwargs.get('reason', None)