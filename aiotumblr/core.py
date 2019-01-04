# encoding=utf-8
from urllib.parse import urlparse

import aiohttp

from oauthlib.oauth1 import Client
from oauthlib.common import urldecode, add_params_to_uri

from .extensions.base import Extension


class AIOTumblr(object):
    api_base_url = 'https://api.tumblr.com/v2/'
    request_token_url = 'https://www.tumblr.com/oauth/request_token'
    authorization_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    def __init__(self, consumer_key: str, consumer_secret: str, resource_owner_key: str = None,
                 resource_owner_secret: str = None, callback_uri: str = None, oauth_verifier: str = None):
        self.session = aiohttp.ClientSession()
        self.oauth_client = Client(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            callback_uri=callback_uri,
            verifier=oauth_verifier,
        )

    async def fetch_request_token(self):
        _, signed_headers, _ = self.oauth_client.sign(self.request_token_url, 'POST')

        resp = await self.session.post(self.request_token_url, headers=signed_headers)
        token_raw = await resp.text()
        token = dict(urldecode(token_raw))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.resource_owner_secret = token['oauth_token_secret']

        # Set callback to None for future signing calls
        self.oauth_client.callback_uri = None

        return token

    def fetch_authorization_url(self, request_token=None):
        if not request_token:
            request_token = self.oauth_client.resource_owner_key

        return f'{self.authorization_url}?oauth_token={request_token}'

    def parse_authorization_response(self, url):
        token = dict(urldecode(urlparse(url).query))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.verifier = token['oauth_verifier']

        return token

    async def fetch_access_token(self, verifier=None):
        if verifier:
            self.oauth_client.verifier = verifier
        if not getattr(self.oauth_client, 'verifier', None):
            raise ValueError('No client verifier set.')  # TODO: implement own exceptions

        _, signed_headers, _ = self.oauth_client.sign(self.access_token_url, 'POST')

        resp = await self.session.post(self.access_token_url, headers=signed_headers)
        token_raw = await resp.text()
        token = dict(urldecode(token_raw))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.resource_owner_secret = token['oauth_token_secret']

        return token

    async def signed_request(self, method: str, endpoint: str, params: dict = None, data: dict = None, json=None,
                             headers: dict = None, **kwargs):
        url = self.api_base_url + endpoint

        if data:
            _, signed_headers, _ = self.oauth_client.sign(
                add_params_to_uri(url, params), http_method=method, body=data, headers=headers
            )
            return await self.session.request(method, url, params=params, data=data, headers=signed_headers)
        elif json:
            # Since it is JSON, body apparently doesn't matter when signing
            _, signed_headers, _ = self.oauth_client.sign(
                add_params_to_uri(url, params), http_method=method, headers=headers
            )
            return await self.session.request(method, url, params=params, json=json, headers=signed_headers)
        else:
            _, signed_headers, _ = self.oauth_client.sign(
                add_params_to_uri(url, params), http_method=method, headers=headers
            )
            return await self.session.request(method, url, params=params, headers=signed_headers)

    @classmethod
    def register_extension(cls, extension: Extension):
        extension.register(cls)

    @classmethod
    def unregister_extension(cls, extension: Extension):
        extension.unregister(cls)
