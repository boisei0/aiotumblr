# encoding=utf-8

# Constants for both APIs:
POST_TYPES = [
    'text',
    'quote',
    'link',
    'answer',
    'video',
    'audio',
    'photo',
    'chat'
]

NPF_POST_STATES = [
    'published',
    'queue',
    'draft',
    'private'
]


class Extension(object):
    def __init__(self, method_prefix: str):
        self.prefix = method_prefix
        raise NotImplementedError()  # TODO

    def register(self, client):
        raise NotImplementedError()

    def unregister(self, client):
        raise NotImplementedError()
