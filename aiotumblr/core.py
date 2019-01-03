# encoding=utf-8
import aiohttp
import asyncio

from oauthlib.oauth1 import Client

from .extensions.base import Extension


class AIOTumblr(object):
    api_base_url = 'https://api.tumblr.com/v2/'
    request_token_url = 'https://www.tumblr.com/oauth/request_token'
    authorization_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    def __init__(self):
        self.session = aiohttp.ClientSession()

    def request(self, method: str, endpoint: str, params: dict = None, data: dict = None, json=None,
                headers: dict = None,
                **kwargs):
        pass

    @classmethod
    def register_extension(cls, extension: Extension):
        extension.register(cls)

    @classmethod
    def unregister_extension(cls, extension: Extension):
        extension.unregister(cls)
