# aiotumblr
The following repository contains the code for `aiotumblr_core`, an OAuth 1.0a API client for Tumblr that runs on top of
`aiohttp`. As a result, the client won't block when running requests.

## Design choices
This client was created with a specific project in mind. Since this project needed to use both the public API as well as
Tumblr's own, undocumented, internal API, the client utilises an extension system. The core client contains all
functions to authorise with Tumblr using the so called 3-legged-authentication system, as well as functions to add 
extensions to the client. Since regular uses will have need nor knowledge of the internal API, it would have been
obnoxious to have the public API available as `TumblrClient.public.endpoint`. For this reason the choice has been made
to patch all methods from the public API on to the base client at runtime. Benchmarks to test the overhead caused by
this still have to be done.

In order to successfully patch methods onto the core client, a couple options were possible. All are unorthodox from a
Python design standard and highly unpythonic. An option would have been to add all functions as methods to an extension
subclass, then register the extension to a private object on the core library and use `__getattr__` to override which
private object to use to call the function from. This would have ended up in runtime overhead for every API call that
would have been made.

Instead there has been chosen to define each endpoint in a `dict` like structure, defining replaceable parts of the
endpoint url, parameters with required as well as optional parts, validators for input, content type of the body
content, validators for body parameters, and so on. This structure gets parsed when registering the extension, and 
functions are generated from the structure. These are then patched on the client. To ease the use for regular users,
it has been chosen to register the Public API extension on the client at import time. This results in a one-time
overhead at runtime to generate the functions. Afterwards, they are available for usage. To ease using them, stubs are
added based on the idea that the Public API extension will always be patched on top of the client.

The Internal API is a different story. Because of bad design choices at Tumblr, the internal API is only secured by
obscurity. The base URL for this API matches the public API. Even worse, registering your own API application will also 
give you access to the internal endpoints. There are a couple differences in the output you might get with your own app
compared to Tumblr's own consumer keys, but the biggest of those is that you will be rate limited as if you were using
the public API. So yeah, security by obscurity. Because of the extension model, `aiotumblr` is able to include the
internal API. Since these endpoints are undocumented it has been created using reverse engineering of the official apps.
For legal reasons the extensions are not publicly included in this repository. In fact, once this library is released to
PyPI, the internal API won't be included. 

Are there no problems with a setup like this? Certainly there are. The stubs included show both arguments as well as
keyword arguments. Internally however these are only keyword arguments for a lack of better way to define them when
generating the functions. This is a likely point of errors for end users. At a future iteration of the library the
possibilities for a different patching method have to be taken in mind, one where the signature seen matches the actual
signature of the function. 
