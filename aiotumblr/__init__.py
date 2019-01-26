# encoding=utf-8
# from .extensions import PublicAPI
from .core import TumblrClient

try:
    from aiotumblr_ext.extensions.public import PublicAPIExtension
    TumblrClient.register_extension(PublicAPIExtension)
except ModuleNotFoundError:
    # Happens when loading the DocGenCommand in the very first setup.py launch, before the public api extension has been
    # installed. [Lena FIXME: figure out a way to handle this cleaner]
    pass
