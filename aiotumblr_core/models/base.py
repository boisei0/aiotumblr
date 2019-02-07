# encoding=utf-8
__all__ = ['BaseModel']

import logging
from dataclasses import dataclass, asdict, fields, is_dataclass
import json

log = logging.getLogger(__name__)


@dataclass
class BaseModel:
    def serialise(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def deserialise(cls, **kwargs) -> 'BaseModel':
        _input = {}
        for field in fields(cls):
            if field.name in kwargs:
                if is_dataclass(field.type):
                    _input[field.name] = field.type.deserialise(**kwargs[field.name])
                else:
                    _input[field.name] = field.type(kwargs[field.name])
            else:
                log.debug(f'Found defined property {field.name!r} on {cls.__name__!r} that is not supplied.')

        # noinspection PyArgumentList
        return cls(**_input)

    # For those who prefer American English
    serialize = serialise

    deserialize = deserialise
