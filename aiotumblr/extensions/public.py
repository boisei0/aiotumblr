# encoding=utf-8
from .base import Extension, POST_TYPES, NPF_POST_STATES
from .utils import create_method, parse_method_info
from ._validators import validate_blog_identifier

METHOD_PREFIX = 'public'
_ENDPOINTS = [
    {
        'method_name': 'get_blog_info',
        'description_summary': 'Retrieve blog info',
        'description_long': 'This method returns general information about the blog, such as the title, number of '
                            'posts, and other high-level data.',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/info',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose the info is requested',
                'validator': validate_blog_identifier
            },
        },
        'params': {},
        'content_type': None,  # options: None/'application/x-www-form-urlencoded'/'application/json'
        'body': None,  # options: None/dict
        'body_type': None,  # options: None/'json'/'kv'
    },
    {
        'method_name': 'get_blog_avatar',
        'description_summary': 'Retrieve a Blog Avatar',
        'description_long': 'Retrieve a Blog Avatar as 64x64 pixel image',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/avatar',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose avatar is requested',
                'validator': validate_blog_identifier
            },
        },
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_avatar_with_size',
        'description_summary': 'Retrieve a Blog Avatar with a specific size',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/avatar/{size}',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose avatar is requested',
                'validator': validate_blog_identifier
            },
            'size': {
                'type': int,
                'description': 'The size of the avatar',
                'validator': lambda x: x in [16, 24, 30, 40, 48, 64, 96, 128, 512]
            }
        },
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_likes',
        'description_summary': 'Retrieve Blog\'s Likes',
        'description_long': 'Retrieve publicly exposed likes from a blog.\n\nNote: Only one of the optional '
                            'parameters `offset`, `before` or `after` can be used\nNote: When requesting posts with '
                            'an offset above 1000, switch to `before` or `after`.',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/likes',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose likes are requested',
                'validator': validate_blog_identifier
            },
        },
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Liked post number to start at',
                'type': int,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'before': {
                'required': False,
                'description': 'Retrieve posts liked before the specified timestamp',
                'type': int,
                'default': None,
            },
            'after': {
                'required': False,
                'description': 'Retrieve posts liked after the specified timestamp',
                'type': int,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_following',
        'description_summary': 'Retrieve Blog\'s following',
        'description_long': 'This method can be used to retrieve the publicly exposed list of blogs that a blog '
                            'follows, in order from most recently-followed to first.',
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/following',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose following is requested',
                'validator': validate_blog_identifier
            },
        },
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Followed blog index to start at',
                'type': int,
                'default': 0,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_followers',
        'description_summary': 'Retrieve a Blog\'s Followers',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/followers',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose followers are requested',
                'validator': validate_blog_identifier,
            },
        },
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Result to start at',
                'type': int,
                'default': 0
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_posts',
        'description_summary': 'Retrieve Published Posts',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose posts are requested',
                'validator': validate_blog_identifier
            },
        },
        'params': {
            'id': {
                'required': False,
                'description': 'A specific post ID. Returns the single post specified or (if not found) a 404 error.',
                'type': int,
                'default': None,
            },
            'tag': {
                'required': False,
                'description': 'Limits the response to posts with the specified tag',
                'type': str,
                'default': None,
            },
            'limit': {
                'required': False,
                'description': 'The number of posts to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Post number to start at',
                'type': int,
                'default': 0,
                # validator? Max offset of 1000? No clue, because it's not documented...
            },
            'reblog_info': {
                'required': False,
                'description': 'Indicates whether to return reblog information. Returns the '
                               'various `reblogged_` fields.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'notes_info': {
                'required': False,
                'description': 'Indicates whether to return notes information (specify true or false). Returns note '
                               'count and note metadata.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'filter': {
                'required': False,
                'description': 'Specifies the post format to return, other than HTML: `text` – Plain text, no HTML; '
                               '`raw` – As entered by the user (no post-processing); if the user writes in Markdown, '
                               'the Markdown will be returned rather than HTML',
                'type': str,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in ['text', 'raw'],
            },
            'before': {
                'required': False,
                'description': 'Returns posts published earlier than a specified Unix timestamp, in seconds.',
                'type': int,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_posts_with_type',
        'description_summary': 'Retrieve Published Posts of a specific type',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/{type}',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose posts are requested',
                'validator': validate_blog_identifier,
            },
        },
        'params': {
            'type': {
                'required': True,
                'description': 'Type of the post',
                'type': str,
                'default': None,
                'validator': lambda x: x in POST_TYPES,
            },
            'id': {
                'required': False,
                'description': 'A specific post ID. Returns the single post specified or (if not found) a 404 error.',
                'type': int,
                'default': None,
            },
            'tag': {
                'required': False,
                'description': 'Limits the response to posts with the specified tag',
                'type': str,
                'default': None,
            },
            'limit': {
                'required': False,
                'description': 'The number of posts to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Post number to start at',
                'type': int,
                'default': 0,
                # validator? Max offset of 1000? No clue, because it's not documented...
            },
            'reblog_info': {
                'required': False,
                'description': 'Indicates whether to return reblog information. Returns the '
                               'various `reblogged_` fields.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'notes_info': {
                'required': False,
                'description': 'Indicates whether to return notes information (specify true or false). Returns note '
                               'count and note metadata.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'filter': {
                'required': False,
                'description': 'Specifies the post format to return, other than HTML: `text` – Plain text, no HTML; '
                               '`raw` – As entered by the user (no post-processing); if the user writes in Markdown, '
                               'the Markdown will be returned rather than HTML',
                'type': str,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in ['text', 'raw'],
            },
            'before': {
                'required': False,
                'description': 'Returns posts published earlier than a specified Unix timestamp, in seconds.',
                'type': int,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_blog_queue',
        'description_summary': 'Retrieve Queued Posts',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/queue',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose queue is requested',
                'validator': validate_blog_identifier,
            },
        },
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Post number to start at',
                'type': int,
                'default': 0,
                # Validator? Max limit of 1000? No clue because look, lack of documentation
            },
            'filter': {
                'required': False,
                'description': 'Specifies the post format to return, other than HTML: text – Plain text, no HTML; '
                               'raw – As entered by the user (no post-processing); if the user writes in Markdown, '
                               'the Markdown will be returned rather than HTML',
                'type': str,
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
        'method_name': 'get_blog_drafts',
        'description_summary': 'Retrieve Draft Posts',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/draft',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose drafts are requested',
                'validator': validate_blog_identifier,
            },
        },
        'params': {
            'before_id': {
                'required': False,
                'description': 'Return posts that have appeared before this ID; Use this parameter to page through '
                               'the results: first get a set of posts, and then get posts since the last ID '
                               'of the previous set.',
                'type': int,
                'default': 0,
            },
            'filter': {
                'required': False,
                'description': 'Specifies the post format to return, other than HTML: text – Plain text, no HTML; '
                               'raw – As entered by the user (no post-processing); if the user writes in Markdown, '
                               'the Markdown will be returned rather than HTML',
                'type': str,
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
        'method_name': 'get_blog_submissions',
        'description_summary': 'Retrieve Submission Posts',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/submission',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose submissions are requested',
                'validator': validate_blog_identifier,
            },
        },
        'params': {
            'offset': {
                'required': False,
                'description': 'Post number to start at',
                'type': int,
                'default': 0
            },
            'filter': {
                'required': False,
                'description': 'Specifies the post format to return, other than HTML: text – Plain text, no HTML; '
                               'raw – As entered by the user (no post-processing); if the user writes in Markdown, '
                               'the Markdown will be returned rather than HTML',
                'type': str,
                'default': None,
                # and if you believe the internals, 'clean' is an option too ¯\_(ツ)_/¯
                'validator': lambda x: x in [None, 'text', 'raw'],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    # TODO: support uploading media
    {
        'method_name': 'create_post',
        'description_summary': 'Create a Post (Neue Post Format)',
        'description_long': 'This methods allows you to create posts (and reblogs) using the Neue Post Format.',
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog to post to',
                'validator': validate_blog_identifier,
            },
        },
        'params': {},
        'content_type': 'application/json',
        'body': {
            'content': {
                'required': True,
                'description': 'An array of NPF content blocks to be used to make the post.',
                'type': list,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'description': 'An array of NPF layout objects to be used to lay out the post content.',
                'type': list,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'description': 'The initial state of the new post, such as `"published"` or `"queued"`. '
                               'Posts can be in the following "states": `"published"` means the post should be '
                               'publicly published immediately, `"queue"` means the post should be added to the '
                               'end of the blog\'s post queue, `"draft"` means the post should be saved as a draft, '
                               '`"private"` means the post should be privately published immediately. If omitted, '
                               'the post will get the state `"published"`',
                'type': str,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'description': 'The exact date and time (ISO 8601 format) to publish the post, if desired. This '
                               'parameter will be ignored unless the state parameter is `"queue"`.',
                'type': str,
                'default': None,
            },
            'tags': {
                'required': False,
                'description': 'A comma-separated list of tags to associate with the post.',
                'type': str,
                'default': None,
            },
            'source_url': {
                'required': False,
                'description': 'A source attribution for the post content.',
                'type': str,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'description': 'Whether or not to share this via any connected Twitter account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'description': 'Whether or not to share this via any connected Facebook account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
        },
        'body_type': 'json',
    },
    {
        'method_name': 'reblog_post',
        'description_summary': 'Reblog a post',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/posts',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog to reblog to',
                'validator': validate_blog_identifier,
            },
        },
        'params': {},
        'content_type': 'application/json',
        'body': {
            'parent_tumblelog_uuid': {
                'required': True,
                'description': 'The unique public identifier of the Tumblelog that\'s being reblogged from.',
                'type': str,
            },
            'parent_post_id': {
                'required': True,
                'description': 'The unique public post ID being reblogged.',
                'type': int,
            },
            'reblog_key': {
                'required': True,
                'description': 'The unique per-post hash validating that this is a genuine reblog action.',
                'type': str,
            },
            'content': {
                'required': True,
                'description': 'An array of NPF content blocks to be used to make the post.',
                'type': list,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'description': 'An array of NPF layout objects to be used to lay out the post content.',
                'type': list,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'description': 'The initial state of the new post, such as `"published"` or `"queued"`. '
                               'Posts can be in the following "states": `"published"` means the post should be '
                               'publicly published immediately, `"queue"` means the post should be added to the '
                               'end of the blog\'s post queue, `"draft"` means the post should be saved as a draft, '
                               '`"private"` means the post should be privately published immediately. If omitted, '
                               'the post will get the state `"published"`',
                'type': str,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'description': 'The exact date and time (ISO 8601 format) to publish the post, if desired. This '
                               'parameter will be ignored unless the state parameter is `"queue"`.',
                'type': str,
                'default': None,
            },
            'tags': {
                'required': False,
                'description': 'A comma-separated list of tags to associate with the post.',
                'type': str,
                'default': None,
            },
            'source_url': {
                'required': False,
                'description': 'A source attribution for the post content.',
                'type': str,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'description': 'Whether or not to share this via any connected Twitter account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'description': 'Whether or not to share this via any connected Facebook account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
            'hide_trail': {
                'required': False,
                'description': 'Whether or not to hide the reblog trail with this new post. Defaults to false.',
                'type': bool,
                'default': False,
            },
        },
        'body_type': 'json',
    },
    {
        'method_name': 'fetch_post',
        'description_summary': 'Fetch an individual post',
        'description_long': None,
        'http_method': 'GET',
        'endpoint': 'blog/{blog_identifier}/posts/{post_id}',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose post is requested',
                'validator': validate_blog_identifier
            },
            'post_id': {
                'type': int,
                'description': 'The ID of the post'
            },
        },
        'params': {},
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'edit_post',
        'description_summary': 'Editing a Post (in NPF format)',
        'description_long': 'This route allows you to edit posts using the Neue Post Format. Note that you can only '
                            'edit posts in NPF if they were originally created in NPF, or are legacy text posts.',
        'http_method': 'PUT',
        'endpoint': 'blog/{blog_identifier}/posts/{post_id}',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose post is requested for editing',
                'validator': validate_blog_identifier
            },
            'post_id': {
                'type': int,
                'description': 'The ID of the post to edit'
            },
        },
        'params': {},
        'content_type': 'application/json',
        'body': {
            'content': {
                'required': True,
                'description': 'An array of NPF content blocks to be used to make the post.',
                'type': list,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'description': 'An array of NPF layout objects to be used to lay out the post content.',
                'type': list,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'description': 'The initial state of the new post, such as `"published"` or `"queued"`. '
                               'Posts can be in the following "states": `"published"` means the post should be '
                               'publicly published immediately, `"queue"` means the post should be added to the '
                               'end of the blog\'s post queue, `"draft"` means the post should be saved as a draft, '
                               '`"private"` means the post should be privately published immediately. If omitted, '
                               'the post will get the state `"published"`',
                'type': str,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'description': 'The exact date and time (ISO 8601 format) to publish the post, if desired. This '
                               'parameter will be ignored unless the state parameter is `"queue"`.',
                'type': str,
                'default': None,
            },
            'tags': {
                'required': False,
                'description': 'A comma-separated list of tags to associate with the post.',
                'type': str,
                'default': None,
            },
            'source_url': {
                'required': False,
                'description': 'A source attribution for the post content.',
                'type': str,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'description': 'Whether or not to share this via any connected Twitter account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'description': 'Whether or not to share this via any connected Facebook account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
        },
        'body_type': 'json'
    },
    {
        'method_name': 'edit_reblog',
        'description_summary': 'Editing a Reblogged Post (in NPF format)',
        'description_long': 'This route allows you to edit reblogs using the Neue Post Format. Note that you can only '
                            'edit posts in NPF if they were originally created in NPF, or are legacy text posts.',

        'http_method': 'PUT',
        'endpoint': 'blog/{blog_identifier}/posts/{post_id}',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose post is requested for editing',
                'validator': validate_blog_identifier
            },
            'post_id': {
                'type': int,
                'description': 'The ID of the post to edit'
            },
        },
        'params': {},
        'content_type': 'application/json',
        'body': {
            'parent_tumblelog_uuid': {
                'required': True,
                'description': 'The unique public identifier of the Tumblelog that\'s being reblogged from.',
                'type': str,
            },
            'parent_post_id': {
                'required': True,
                'description': 'The unique public post ID being reblogged.',
                'type': int,
            },
            'reblog_key': {
                'required': True,
                'description': 'The unique per-post hash validating that this is a genuine reblog action.',
                'type': str,
            },
            'content': {
                'required': True,
                'description': 'An array of NPF content blocks to be used to make the post.',
                'type': list,
                'validator': lambda x: isinstance(x, list),
            },
            'layout': {
                'required': False,
                'description': 'An array of NPF layout objects to be used to lay out the post content.',
                'type': list,
                'default': [],
                'validator': lambda x: isinstance(x, list),
            },
            'state': {
                'required': False,
                'description': 'The initial state of the new post, such as `"published"` or `"queued"`. '
                               'Posts can be in the following "states": `"published"` means the post should be '
                               'publicly published immediately, `"queue"` means the post should be added to the '
                               'end of the blog\'s post queue, `"draft"` means the post should be saved as a draft, '
                               '`"private"` means the post should be privately published immediately. If omitted, '
                               'the post will get the state `"published"`',
                'type': str,
                'default': 'published',
                'validator': lambda x: x in NPF_POST_STATES,
            },
            'publish_on': {
                'required': False,
                'description': 'The exact date and time (ISO 8601 format) to publish the post, if desired. This '
                               'parameter will be ignored unless the state parameter is `"queue"`.',
                'type': str,
                'default': None,
            },
            'tags': {
                'required': False,
                'description': 'A comma-separated list of tags to associate with the post.',
                'type': str,
                'default': None,
            },
            'source_url': {
                'required': False,
                'description': 'A source attribution for the post content.',
                'type': str,
                'default': None,
            },
            'send_to_twitter': {
                'required': False,
                'description': 'Whether or not to share this via any connected Twitter account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['twitter_send']
            },
            'send_to_facebook': {
                'required': False,
                'description': 'Whether or not to share this via any connected Facebook account on post publish. '
                               'Defaults to the blog\'s global setting.',
                'type': bool,
                'default': False,  # no but actually, get_user_info()[blog_identifier]['facebook_send']
            },
            'hide_trail': {
                'required': False,
                'description': 'Whether or not to hide the reblog trail with this new post. Defaults to false.',
                'type': bool,
                'default': False,
            },
        },
        'body_type': 'json'
    },
    {
        'method_name': 'delete_post',
        'description_summary': 'Delete a Post',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'blog/{blog_identifier}/post/delete',
        'url_parameters': {
            'blog_identifier': {
                'type': str,
                'description': 'The blog whose post has to be deleted',
                'validator': validate_blog_identifier
            },
        },
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
                'description': 'The ID of the post to delete',
                'type': int,
            },
        },
        'body_type': 'kv',
    },
    {
        'method_name': 'get_user_info',
        'description_summary': 'Get a User\'s Information',
        'description_long': 'Use this method to retrieve the user\'s account information that matches the OAuth '
                            'credentials submitted with the request.',
        'http_method': 'GET',
        'endpoint': 'user/info',
        'url_parameters': {},
        'params': {
            # None in the public API, internal mentions keys `force_oauth=false` and `private_blogs=true`
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_user_dashboard',
        'description_summary': 'Retrieve a User\'s Dashboard',
        'description_long': 'Use this method to retrieve the dashboard that matches the OAuth credentials '
                            'submitted with the request.',
        'http_method': 'GET',
        'endpoint': 'user/dashboard',
        'url_parameters': {},
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Post number to start at',
                'type': int,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'type': {
                'required': False,
                'description': 'The type of post to return. Specify one of the following: text, photo, quote, '
                               'link, chat, audio, video, answer',
                'type': str,
                'default': None,
                'validator': lambda x: x in POST_TYPES,
            },
            'since_id': {
                'required': False,
                'description': 'Return posts that have appeared after this ID; Use this parameter to page through '
                               'the results: first get a set of posts, and then get posts since the last ID of the '
                               'previous set.',
                'type': int,
                'default': 0,
            },
            'reblog_info': {
                'required': False,
                'description': 'Indicates whether to return reblog information (specify true or false). Returns the '
                               'various `reblogged_` fields.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
            'notes_info': {
                'required': False,
                'description': 'Indicates whether to return notes information (specify true or false). Returns '
                               'note count and note metadata.',
                'type': bool,
                'default': False,
                'validator': lambda x: x in [True, False],
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_user_likes',
        'description_summary': 'Retrieve a User\'s Likes',
        'description_long': 'Use this method to retrieve the liked posts that match the OAuth credentials submitted '
                            'with the request. You can only provide either before, after, or offset. If you provide '
                            'more than one of these options together you will get an error. You can still use limit '
                            'with any of those three options to limit your result set. When using the offset parameter '
                            'the maximum limit on the offset is 1000. If you would like to get more results than that '
                            'use either before or after.',
        'http_method': 'GET',
        'endpoint': 'user/likes',
        'url_parameters': {},
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Liked post number to start at',
                'type': int,
                'default': 0,
                'validator': lambda x: x < 1000,
            },
            'before': {
                'required': False,
                'description': 'Retrieve posts liked before the specified timestamp',
                'type': int,
                'default': None,
            },
            'after': {
                'required': False,
                'description': 'Retrieve posts liked after the specified timestamp',
                'type': int,
                'default': None,
            },
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'get_user_following',
        'description_summary': 'Retrieve the Blogs a User Is Following',
        'description_long': 'Use this method to retrieve the blogs followed by the user whose OAuth credentials are '
                            'submitted with the request.',
        'http_method': 'GET',
        'endpoint': 'user/following',
        'url_parameters': {},
        'params': {
            'limit': {
                'required': False,
                'description': 'The number of results to return: 1–20, inclusive',
                'type': int,
                'default': 20,
                'validator': lambda x: 1 <= x <= 20,
            },
            'offset': {
                'required': False,
                'description': 'Result number to start at',
                'type': int,
                'default': 0,
            }
        },
        'content_type': None,
        'body': None,
        'body_type': None,
    },
    {
        'method_name': 'follow_blog',
        'description_summary': 'Follow a blog',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'user/follow',
        'url_parameters': {},
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'url': {
                'required': True,
                'description': 'The URL of the blog to follow',
                'type': str,
                'validator': lambda x: x.endswith('.tumblr.com'),
            },
        },
        'body_type': 'kv',
    },
    {
        'method_name': 'unfollow_blog',
        'description_summary': 'Unfollow a blog',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'user/unfollow',
        'url_parameters': {},
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'url': {
                'required': True,
                'description': 'The URL of the blog to unfollow',
                'type': str,
                'validator': lambda x: x.endswith('.tumblr.com'),
            },
        },
        'body_type': 'kv',
    },
    {
        'method_name': 'like_post',
        'description_summary': 'Like a Post',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'user/like',
        'url_parameters': {},
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
                'description': 'The ID of the post to like',
                'type': int,
            },
            'reblog_key': {
                'required': True,
                'description': 'The reblog key for the post id',
                'type': str,
            },
        },
        'body_type': 'kv',
    },
    {
        'method_name': 'unlike_post',
        'description_summary': 'Unlike a Post',
        'description_long': None,
        'http_method': 'POST',
        'endpoint': 'user/unlike',
        'url_parameters': {},
        'params': {},
        'content_type': 'application/x-www-form-urlencoded',
        'body': {
            'id': {
                'required': True,
                'description': 'The ID of the post to unlike',
                'type': int,
            },
            'reblog_key': {
                'required': True,
                'description': 'The reblog key for the post id',
                'type': str,
            },
        },
        'body_type': 'kv',
    },
]


class PublicAPI(Extension):
    prefix = METHOD_PREFIX

    @classmethod
    def register(cls, client):
        for method_info in _ENDPOINTS:
            params, body = parse_method_info(method_info)
            create_method(client, params, body, method_info)

    @classmethod
    def unregister(cls, client):
        for method_info in _ENDPOINTS:
            delattr(client, method_info['method_name'])
