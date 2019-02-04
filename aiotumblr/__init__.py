# encoding=utf-8
from .extensions import PublicAPI
from .core import TumblrClient

TumblrClient.register_extension(PublicAPI)

