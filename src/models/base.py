import copy
import yaml
import json

class Base(object):
    __slots__ = ()
    
    #-------------------------------------------------------------------------------
    def __str__(self):
        return self.name
    #-------------------------------------------------------------------------------
    @classmethod
    def _from_dict(cls, d):
        return cls(**d)
    #-------------------------------------------------------------------------------
    # This will need recursive functionality for nested objects.
    #-------------------------------------------------------------------------------
    def _to_dict(self): 
        dictObj = dict()
        
        for key in self.__slots__:
            obj = getattr(self, key)
            if obj is None:
                continue
            dictObj[key] = self.traverse(obj)
        return dictObj

    #-------------------------------------------------------------------------------
    def traverse(self, obj):
        if isinstance(obj, Base):
            return obj._to_dict()
        if isinstance(obj, dict):
            return {k: self.traverse(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.traverse(x) for x in obj]
        return obj

    #-------------------------------------------------------------------------------
    @classmethod
    def _from_json(cls, s):
        return cls._from_dict(json.loads(s))
    #-------------------------------------------------------------------------------
    def _to_json(self):
        return json.dumps(self._to_dict())
    #-------------------------------------------------------------------------------
    @classmethod
    def _from_yaml(cls, s):
        return cls._from_dict(yaml.load(s))
    #-------------------------------------------------------------------------------
    def _to_yaml(self):
        return yaml.dump(self._to_dict())
    #-------------------------------------------------------------------------------
    def copy(self):
        return copy.deepcopy(self)
    #-------------------------------------------------------------------------------
    def _create_error_message(self, error_message, dump):
        header = f'{self.__class__.__name__}: {error_message}'
        if isinstance(dump, dict):
            body = json.dumps(dump, indent=4)
        if isinstance(dump, str):
            body = dump
        if isinstance(dump, list):
            body = '\n'.join(dump)

        return f'{header}\n{body}'

#-------------------------------------------------------------------------------------------
class BaseResourceObject(Base):
    __slots__ = ()

#-------------------------------------------------------------------------------------------
class BaseEventObject(Base):
    __slots__ = ()