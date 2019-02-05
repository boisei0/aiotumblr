# encoding=utf-8
from typing import Callable
from forge import repr_callable

from aiotumblr_core.extensions.utils import parse_method_info, generate_docstring, format_docstring_for_sphinx

__all__ = ['POST_TYPES', 'NPF_POST_STATES', 'Extension']

# Base endpoint design:
# {
#     'method_name': '',
#     'description_summary': '',
#     'description_long': None,
#     'http_method': 'POST'
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
    prefix = ''

    @classmethod
    def register(cls, client):
        raise NotImplementedError()

    @classmethod
    def unregister(cls, client):
        raise NotImplementedError()

    @classmethod
    def generate_docs(cls):
        raise NotImplementedError()

    @classmethod
    def _generate_doc(cls, method_info):
        params, body = parse_method_info(method_info)
        method_doc = generate_docstring(params, body, method_info)
        doc = f".. py:method:: {method_info['method_name']}(...)\n\n"  # FIXME
        doc += format_docstring_for_sphinx(method_doc, indent=3)
        return doc

    @classmethod
    def _generate_doc_from_method(cls, method: Callable):
        doc = f".. py:method:: {repr_callable(method)}\n\n"
        doc += format_docstring_for_sphinx(method.__doc__, indent=3)
        return doc
