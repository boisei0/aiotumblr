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
    @classmethod
    def register(cls, client):
        raise NotImplementedError()

    @classmethod
    def unregister(cls, client):
        raise NotImplementedError()
