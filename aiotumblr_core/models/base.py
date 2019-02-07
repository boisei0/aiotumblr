# encoding=utf-8
__all__ = ['BaseModel']

from dataclasses import dataclass, asdict
import json


@dataclass
class BaseModel:
    def serialise(self):
        json.dumps(asdict(self))

    @classmethod
    def deserialise(cls, **kwargs):
        raise NotImplemented

    # For those who prefer American English
    serialize = serialise

    deserialize = deserialise
