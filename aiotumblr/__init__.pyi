# encoding=utf-8
# Stubs for the aiotumblr.TumblrClient core class, with the idea that the public API is already hooked on it
from typing import Dict, List, Tuple, Optional, Any, Union
from aiohttp import ClientResponse

from .extensions import Extension

class TumblrClient:
    def __init__(self, consumer_key: str, consumer_secret: str, resource_owner_key: str = None,
                 resource_owner_secret: str = None, callback_uri: str = None, oauth_verifier: str = None): ...

    async def fetch_request_token(self) -> Dict[str, str]: ...

    def fetch_authorization_url(self, request_token: str = None) -> str: ...

    def parse_authorization_response(self, url: str) -> Dict[str, str]: ...

    async def fetch_access_token(self, verifier: str = None) -> Dict[str, str]: ...

    async def signed_request(self, method: str, endpoint: str, params: Optional[List[Tuple[str, str]]] = None,
                             data: Optional[Dict[str, str]] = None, json: Optional[Any] = None,
                             headers: Optional[Dict[str, str]] = None, **kwargs) -> ClientResponse: ...

    @classmethod
    def register_extension(cls, extension: Extension): ...

    @classmethod
    def unregister_extension(cls, extension: Extension): ...

    # The following methods are defined dynamically in aiotumblr.extensions.public
    async def get_blog_info(self, blog_identifier: str) -> ClientResponse: ...

    async def get_blog_avatar(self, blog_identifier: str) -> ClientResponse: ...

    async def get_blog_avatar_with_size(self, blog_identifier: str, size: Union[str, int]) -> ClientResponse: ...

    async def get_blog_likes(self, blog_identifier: str, limit: Optional[int] = None, offset: Optional[int] = None,
                             before: Optional[int] = None, after: Optional[int] = None) \
            -> ClientResponse: ...

    async def get_blog_following(self, blog_identifier: str, limit: Optional[int] = None,
                                 offset: Optional[int] = None) \
            -> ClientResponse: ...

    async def get_blog_followers(self, blog_identifier: str, limit: Optional[int] = None,
                                 offset: Optional[int] = None) \
            -> ClientResponse: ...

    async def get_blog_posts(self, blog_identifier: str, type: Optional[str] = None, id: Optional[int] = None,
                             tag: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None,
                             reblog_info: Optional[bool] = None, notes_info: Optional[bool] = None,
                             filter: Optional[str] = None, before: Optional[int] = None) \
            -> ClientResponse: ...

    async def get_blog_queue(self, blog_identifier: str, limit: Optional[int] = None, offset: Optional[int] = None,
                             filter: Optional[str] = None) \
            -> ClientResponse: ...

    async def get_blog_drafts(self, blog_identifier: str, before_id: Optional[int] = None,
                              filter: Optional[str] = None) \
            -> ClientResponse: ...

    async def get_blog_submission(self, blog_identifier: str, offset: Optional[int] = None,
                                  filter: Optional[str] = None) \
            -> ClientResponse: ...

    async def create_post(self, blog_identifier: str, content: List[Dict[str, Any]],
                          layout: Optional[List[Dict[str, Any]]] = None, state: Optional[str] = None,
                          publish_on: Optional[str] = None, tags: Optional[str] = None,
                          source_url: Optional[str] = None, send_to_twitter: Optional[bool] = None,
                          send_to_facebook: Optional[bool] = None) \
            -> ClientResponse: ...

    async def reblog_post(self, blog_identifier: str, parent_tumblelog_uuid: str, parent_post_id: int, reblog_key: str,
                          content: List[Dict[str, Any]], layout: Optional[List[Dict[str, Any]]] = None,
                          state: Optional[str] = None, publish_on: Optional[str] = None, tags: Optional[str] = None,
                          source_url: Optional[str] = None, send_to_twitter: Optional[bool] = None,
                          send_to_facebook: Optional[bool] = None, hide_trail: Optional[bool] = None) \
            -> ClientResponse: ...

    async def fetch_post(self, blog_identifier: str, post_id: int) -> ClientResponse: ...

    async def delete_post(self, blog_identifier: str, id: int) -> ClientResponse: ...

    async def get_user_info(self) -> ClientResponse: ...

    async def get_user_dashboard(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                 type: Optional[str] = None, since_id: Optional[int] = None,
                                 reblog_info: Optional[bool] = None, notes_info: Optional[bool] = None) \
            -> ClientResponse: ...

    async def get_user_likes(self, limit: Optional[int] = None, offset: Optional[int] = None,
                             before: Optional[int] = None, after: Optional[int] = None) \
            -> ClientResponse: ...

    async def get_user_following(self, limit: Optional[int] = None, offset: Optional[int] = None) -> ClientResponse: ...

    async def follow_blog(self, url: str) -> ClientResponse: ...

    async def unfollow_blog(self, url: str) -> ClientResponse: ...

    async def like_post(self, id: int, reblog_key: str) -> ClientResponse: ...

    async def unike_post(self, id: int, reblog_key: str) -> ClientResponse: ...
