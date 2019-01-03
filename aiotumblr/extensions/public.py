# encoding=utf-8
from .base import Extension, POST_TYPES, NPF_POST_STATES

METHOD_PREFIX = 'public'
endpoints = [
    {
        'method_name': 'get_blog_info',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/info',
        'url_parameters': ['blog_identifier'],
        'params': {},
        'content_type': None,  # options: None/'application/x-www-form-urlencoded'/'application/json'
        'body': None,  # options: None/dict
        'body_type': None,  # options: None/'json'/'kv'
    },
    {
        'method_name': 'get_blog_avatar',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/avatar',
        'url_parameters': ['blog_identifier'],
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_avatar_with_size',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/avatar/{size}',
        'url_parameters': ['blog_identifier', 'size'],
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_likes',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/likes',
        'url_parameters': ['blog_identifier'],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'before': {
                'required': False,
                'default': None,
            },
            'after': {
                'required': False,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_blog_following',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/following',
        'url_parameters': ['blog_identifier'],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_blog_followers',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/followers',
        'url_parameters': ['blog_identifier'],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0
            },
        },
        'content_type': None,
        'body': None,
        'Body_type': None,
    },
    {
        'method': 'get_blog_posts',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': ['blog_identifier'],
        'params': {
            'type': {
                'required': False,
                'default': None,
                'validator': lambda x: x in POST_TYPES,
            },
            'id': {
                'required': False,
                'default': None,
            },
            'tag': {
                'required': False,
                'default': None,
            },
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
                # validator? Max offset of 1000? No clue, because it's not documented...
            },
            'reblog_info': {
                'required': False,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'notes_info': {
                'required': False,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'filter': {
                'required': False,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in [None, 'text', 'raw'],
            },
            'before': {
                'required': False,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_blog_queue',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/queue',
        'url_parameters': ['blog_identifier'],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
                # Validator? Max limit of 1000? No clue because look, lack of documentation
            },
            'filter': {
                'required': False,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in [None, 'text', 'raw'],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_blog_drafts',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/draft',
        'url_parameters': ['blog_identifier'],
        'params': {
            'before_id': {
                'required': False,
                'default': 0,
            },
            'filter': {
                'required': False,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in [None, 'text', 'raw'],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_blog_submissions',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/submission',
        'url_parameters': ['blog_identifier'],
        'params': {
            'offset': {
                'required': False,
                'default': 0
            },
            'filter': {
                'required': False,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in [None, 'text', 'raw'],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'create_post',
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': ['blog_identifier'],
        'params': {},
        'content_type': 'application/json',
        'body': {
            'content': {
                'required': True,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'default': None,
            },
            'tags': {
                'required': False,
                'default': None,
            },
            'source_url': {
                'required': False,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
        },
        'body_type': 'json',
    },
    {
        'method': 'reblog_post',
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': ['blog_identifier'],
        'params': {},
        'content_type': 'application/json',
        'body': {
            'parent_tumblelog_uuid': {
                'required': True,
            },
            'parent_post_id': {
                'required': True,
            },
            'reblog_key': {
                'required': True,
            },
            'content': {
                'required': True,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'default': None,
            },
            'tags': {
                'required': False,
                'default': None,
            },
            'source_url': {
                'required': False,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
            'hide_trail': {
                'required': False,
                'default': False,
            },
        },
        'body_type': 'json',
    },
    {
        'method': 'fetch_post',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/{post_id}',
        'url_parameters': ['blog_identifier', 'post_id'],
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'edit_post',
        'http_method': 'PUT',
        'endpoint': 'blog/{blog_identifier}/posts/{post_id}',
        'url_parameters': ['blog_identifier', 'post_id'],
        'params': {},
        'content_type': 'application/json',
        'body': {},  # TODO: implement from create_post/reblog_post
        'body_type': 'json'
    },
    {
        'method': 'delete_post',
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/post/delete',
        'url_parameters': ['blog_identifier'],
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
            },
        },
        'body_type': 'kv',
    },
    {
        'method': 'get_user_info',
        'http_method': 'GET',
        'endpoint': 'user/info',
        'url_parameters': [],
        'params': {
            # None in the public API, internal mentions keys `force_oauth=false` and `private_blogs=true`
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_user_dashboard',
        'http_method': 'GET',
        'endpoint': 'user/dashboard',
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'type': {
                'required': False,
                'default': None,
                'validator': lambda x: x in POST_TYPES,
            },
            'since_id': {
                'required': False,
                'default': 0,
            },
            'reblog_info': {
                'required': False,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'notes_info': {
                'required': False,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_user_likes',
        'http_method': 'GET',
        'endpoint': 'user/likes',
        'url_parameters': [],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'before': {
                'required': False,
                'default': None,
            },
            'after': {
                'required': False,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'get_user_following',
        'http_method': 'GET',
        'endpoint': 'user/following',
        'url_parameters': [],
        'params': {
            'limit': {
                'required': False,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'default': 0,
            }
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method': 'follow_blog',
        'http_method': 'POST',
        'endpoint': 'user/follow',
        'url_parameters': [],
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'url': {
                'required': True,
            },
        },
        'body_type': 'kv',
    },
    {
        'method': 'unfollow_blog',
        'http_method': 'POST',
        'endpoint': 'user/unfollow',
        'url_parameters': [],
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'url': {
                'required': True,
            },
        },
        'body_type': 'kv',
    },
    {
        'method': 'like_post',
        'http_method': 'POST',
        'endpoint': 'user/like',
        'url_parameters': [],
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
            },
            'reblog_key': {
                'required': True
            },
        },
        'body_type': 'kv',
    },
    {
        'method': 'unlike_post',
        'http_method': 'POST',
        'endpoint': 'user/unlike',
        'url_parameters': [],
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
            },
            'reblog_key': {
                'required': True
            },
        },
        'body_type': 'kv',
    },
]


class PublicAPI(Extension):
    def __init__(self):
        super().__init__(METHOD_PREFIX)

    @classmethod
    def register(cls, client):
        for method_info in endpoints:
            _params = method_info['params']
            if _params:
                pass  # TODO: continue here

            # async def method(self, *args, **kwargs):
            #     client.request(method_info['http_method'], method_info['endpoint'], )
            #
            # setattr(client, method_info['method'], method)
        pass
