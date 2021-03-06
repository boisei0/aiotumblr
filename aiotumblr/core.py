# encoding=utf-8
from typing import Dict, List, Tuple, Any, Optional, Type
from urllib.parse import urlparse

import aiohttp

from oauthlib.oauth1 import Client
from oauthlib.common import urldecode, add_params_to_uri

from .extensions.base import Extension
from aiotumblr.utils.tracers import AIOTumblrDebugger

import logging

__all__ = ['TumblrClient']

log = logging.getLogger(__name__)


class TumblrClient(object):
    api_base_url = 'https://api.tumblr.com/v2/'
    request_token_url = 'https://www.tumblr.com/oauth/request_token'
    authorization_url = 'https://www.tumblr.com/oauth/authorize'
    access_token_url = 'https://www.tumblr.com/oauth/access_token'

    def __init__(self, consumer_key: str, consumer_secret: str, resource_owner_key: Optional[str] = None,
                 resource_owner_secret: Optional[str] = None, callback_uri: Optional[str] = None,
                 oauth_verifier: Optional[str] = None, debug_mode: Optional[bool] = None):
        if debug_mode:
            self.session = aiohttp.ClientSession(trace_configs=[AIOTumblrDebugger(logger=log)])
        else:
            self.session = aiohttp.ClientSession()

        self.oauth_client = Client(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            callback_uri=callback_uri,
            verifier=oauth_verifier,
        )

    async def fetch_request_token(self) -> Dict[str, str]:
        log.debug(f'Fetching request token...')
        _, signed_headers, _ = self.oauth_client.sign(self.request_token_url, 'POST')
        log.debug(f'Signed headers: {signed_headers}')

        resp = await self.session.post(self.request_token_url, headers=signed_headers)
        log.debug(f'Response: {resp.status} {resp.reason}')
        log.debug(f'To: {resp.method} {resp.real_url.human_repr()}')
        log.debug(f'Requested as: {resp.request_info.method} {resp.request_info.real_url.human_repr()}')
        log.debug(f'Request headers: {resp.request_info.headers}')

        token_raw = await resp.text()
        log.debug(f'Token response: {token_raw}')
        token = dict(urldecode(token_raw))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.resource_owner_secret = token['oauth_token_secret']

        # Set callback to None for future signing calls
        self.oauth_client.callback_uri = None

        return token

    def fetch_authorization_url(self, request_token: str = None) -> str:
        if not request_token:
            request_token = self.oauth_client.resource_owner_key

        return f'{self.authorization_url}?oauth_token={request_token}'

    def parse_authorization_response(self, url: str) -> Dict[str, str]:
        token = dict(urldecode(urlparse(url).query))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.verifier = token['oauth_verifier']

        return token

    async def fetch_access_token(self, verifier: Optional[str] = None) -> Dict[str, str]:
        if verifier:
            self.oauth_client.verifier = verifier
        if not getattr(self.oauth_client, 'verifier', None):
            raise ValueError('No client verifier set.')  # TODO: implement own exceptions

        log.debug(f'Fetching access token...')
        _, signed_headers, _ = self.oauth_client.sign(self.access_token_url, 'POST')
        log.debug(f'Signed headers: {signed_headers}')

        resp = await self.session.post(self.access_token_url, headers=signed_headers)
        log.debug(f'Response: {resp.status} {resp.reason}')
        log.debug(f'To: {resp.method} {resp.real_url.human_repr()}')
        log.debug(f'Requested as: {resp.request_info.method} {resp.request_info.real_url.human_repr()}')
        log.debug(f'Request headers: {resp.request_info.headers}')

        token_raw = await resp.text()
        log.debug(f'Token response: {token_raw}')
        token = dict(urldecode(token_raw))

        self.oauth_client.resource_owner_key = token['oauth_token']
        self.oauth_client.resource_owner_secret = token['oauth_token_secret']

        # Unset verifier
        self.oauth_client.verifier = None

        return token

    async def signed_request(self, method: str, endpoint: str, params: Optional[List[Tuple[str, str]]] = None,
                             data: Optional[Dict[str, str]] = None, json: Optional[Any] = None,
                             headers: Optional[Dict[str, str]] = None, **kwargs) -> aiohttp.ClientResponse:
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
    def register_extension(cls, extension: Type[Extension]):
        extension.register(cls)

    @classmethod
    def unregister_extension(cls, extension: Type[Extension]):
        extension.unregister(cls)

    async def close_connection(self):
        await self.session.close()
