==================
Writing extensions
==================
AIOTumblr defines its own extension syntax. For this rather unorthodox structure has been chosen to separate the public,
documented Tumblr API from the internal, undocumented API. The public API is released with the package. The internal
API can be installed from separate packages, but is not included with the default release.

Since the internal API extensions won't be made available to the general public, the base library shouldn't have to
suffer from additional namespaces added purely for users who have access to the internal API. The base library comes
with functions to register extensions to it. These extensions are then patched on top of the base library, providing
direct access to the methods. The methods are generated at runtime from a standardised method format:

.. code-block:: python

   method = {
       'method_name': '',
       'description_summary': '',
       'description_long': None,
       'http_method': 'POST'
       'endpoint': '',  # str ready to be used with f.format
       'url_parameters': {  # dict with key/value pairs where each key is a variable in `endpoint`
           'key': {
               'type': str,
               'description': '',
               'validator': lambda x: True,
           },
       },
       'params': {  # dict with key/value pairs or {}
           'key': {
               'required': False,
               'description': '',
               'type': int,
               'default': 0,
               'validator': lambda x: True,
           },
       },
       'content_type': 'application/x-www-form-urlencoded',  # content-type or None
       'body': {  # dict with key/value pairs or None
           'key': {
               'required': True,
               'description': '',
               'type': str,
               'default': 'foo',
               'validator': lambda x: True,
           },
       },
       'body_type': 'kv',  # 'kv', 'json' or None
   }

AIOTumblr defines a couple functions in `aiotumblr.extensions.utils` to create methods and documentation from this
formatting. Below is a sample extension defined.

.. todo:: Improve this with actual documentation rather than examples

.. code-block:: python

   class SampleExtension(aiotumblr.extensions.Extension):
       prefix = 'sample'

       @classmethod
       def register(cls, client):
           params, body = aiotumblr.extensions.utils.parse_method_info(method)
           create_method(client, params, body, method)

       @classmethod
       def unregister(cls, client):
           delattr(client, method['method_name'])

       @classmethod
       def generate_docs(cls):
           _title = 'sample extension'
           doc = f"""{len(_title) * '='}
   {_title}
   {len(_title) * '='}\n\n"""
           from aiotumblr.core import TumblrClient
           from asyncio import get_event_loop()
           loop = get_event_loop()
           t = TumblrClient('placeholder', 'placeholder')
           t.register_extension(cls)
           doc += cls._generate_doc_from_method(t, method['method_name'])
           doc += '\n'

           loop.run_until_complete(t.close_connection())
           return doc

Extension packages
==================
Starting with AIOTumblr 0.2, extensions are moving to their own packages to decrease the footprint of the base library.
The following describes the layout of extension packages, following PEP420::

    root
        aiotumblr_ext
            extensions
                <extension_name>
                    __init__.py
        setup.py

`aiotumblr_ext` functions as root namespace package, `aiotumblr_ext.extensions` is a namespace package as well. Make
sure the `__init__.py` is defined in the right place. In the near future when models are added, these will be defined
as namespace package on `aiotumblr_ext.models`.