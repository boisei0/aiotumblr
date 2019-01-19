# encoding=utf-8

# Base endpoint design:
# {
#     'method_name': '',
#     'description_summary': '',
#     'description_long': None,
#     'endpoint': '',  # str ready to be used with f.format
#     'url_parameters': {  # dict with key/value pairs where each key is a variable in `endpoint`
#         'key': {
#             'type': str,
#             'description': '',
#             'validator': lambda x: True,
#         },
#     },
#     'params': {  # dict with key/value pairs or {}  # TODO revise "or {}", cf `body`
#         'key': {
#             'required': False,
#             'description': '',
#             'type': int,
#             'default': 0,
#             'validator': lambda x: True,
#         },
#     },
#     'content_type': 'application/x-www-form-urlencoded',  # content-type or None
#     'body': {  # dict with key/value pairs or None
#         'key': {
#             'required': True,
#             'description': '',
#             'type': str,
#             'default': 'foo',
#             'validator': lambda x: True,
#         },
#     },
#     'body_type': 'kv',  # 'kv', 'json' or None
# }

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
