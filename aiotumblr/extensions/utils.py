# encoding=utf-8
from typing import Dict, Any, Tuple, Union


def format_parameter(param):
    if isinstance(param, bool):
        return str(param).lower()
    return param


def parse_method_info(method_info: Dict[str, Any]) -> Tuple[Dict[str, Union[list, Any]], Dict[str, Union[list, Any]]]:
    _params = method_info['params']
    _required_params = []
    _optional_params = []
    if _params:
        for _param, val in _params.items():
            if val['required']:
                _required_params.append(_param)
            else:
                _optional_params.append(_param)

    _body = method_info['body']
    _required_body = []
    _optional_body = []
    if _body:
        for _key, val in _body.items():
            if val['required']:
                _required_body.append(_key)
            else:
                _optional_body.append(_key)

    params = {
        'required': _required_params,
        'optional': _optional_params,
        'data': _params,
    }
    body = {
        'required': _required_body,
        'optional': _optional_body,
        'data': _body
    }

    return params, body


def generate_docstring(params, body, method_info) -> str:
    try:
        ds_url_params = '\n'.join(f""":param {key}: {url_param['description']}
:type {key} {url_param['type'].__name__}""" for key, url_param in method_info['url_parameters'].items())
    except (TypeError, KeyError):
        print(method_info)
        raise

    required_params = []
    for key in params['required']:
        req_param = params['data'][key]
        required_params.append(f""":param {key}: {req_param['description']}
:type {key}: {req_param['type'].__name__}""")
    ds_required_params = '\n'.join(required_params)

    optional_params = []
    for key in params['optional']:
        opt_param = params['data'][key]
        optional_params.append(f""":param {key}: {opt_param['description']}
:type {key}: {opt_param['type'].__name__} or None""")
    ds_optional_params = '\n'.join(optional_params)

    required_body_args = []
    for key in body['required']:
        req_body_arg = body['data'][key]
        required_body_args.append(f""":param {key}: {req_body_arg['description']}
:type {key}: {req_body_arg['type'].__name__}""")
    ds_required_body_args = '\n'.join(required_body_args)

    optional_body_args = []
    for key in body['optional']:
        opt_body_arg = body['data'][key]
        optional_body_args.append(f""":param {key}: {opt_body_arg['description']}
:type {key}: {opt_body_arg['type'].__name__} or None""")
    ds_optional_body_args = '\n'.join(optional_body_args)

    # TODO: Is there an easy way to DRY this without an additional dependency as Jinja?
    if method_info['description_long']:
        return f"""{method_info['description_summary']}

{method_info['description_long']}

{ds_url_params}
{ds_required_params}
{ds_optional_params}
{ds_required_body_args}
{ds_optional_body_args}
:return: API response for {method_info['method_name']}
:rtype: `aiohttp.ClientResponse`
:raises SyntaxError: if required parameter is missing
:raises ValueError: if supplied parameter fails validation
"""
    else:
        return f"""{method_info['description_summary']}

{ds_url_params}
{ds_required_params}
{ds_optional_params}
{ds_required_body_args}
{ds_optional_body_args}
:return: API response for {method_info['method_name']}
:rtype: `aiohttp.ClientResponse`
:raises SyntaxError: if required parameter is missing
:raises ValueError: if supplied parameter fails validation
"""


def create_method(client, params, body, method_info):
    async def inner_method(self, **kwargs):
        # Verify signature
        endpoint_signature = {}
        for url_param, url_param_info in method_info['url_parameters'].items():
            if url_param not in kwargs:
                raise SyntaxError(f'Argument {url_param!r} is a required keyword argument.')

            if 'validator' in url_param_info:
                tested = url_param_info['validator'](kwargs[url_param])
                if not tested:
                    # TODO: less generic error messages by abstracting this to the endpoint data structure
                    raise ValueError(f'Supplied argument {url_param!r} failed to validate')

            endpoint_signature[url_param] = kwargs[url_param]
        endpoint = method_info['endpoint'].format(**endpoint_signature)

        # Verify params
        # TODO: DRY
        params_signature = []
        for param in params['required']:
            item = None

            if param not in kwargs:
                if 'default' not in params['data'][param]:
                    raise SyntaxError(f'Parameter {param!r} is a required keyword argument')
                else:
                    item = params['data'][param]

            if not item:
                item = kwargs[param]

            if 'validator' in params['data'][param]:
                tested = params['data'][param]['validator'](item)
                if not tested:
                    # TODO: less generic error messages by abstracting this to the endpoint data structure
                    raise ValueError(f'Supplied argument {param!r} failed to validate')

            params_signature.append((param, format_parameter(item)))
        for param in params['optional']:
            if param in kwargs:
                if 'validator' in params['data'][param]:
                    tested = params['data'][param]['validator'](kwargs[param])
                    if not tested:
                        # TODO: less generic error messages by abstracting this to the endpoint data structure
                        raise ValueError(f'Supplied argument {param!r} failed to validate')

                params_signature.append((param, format_parameter(kwargs[param])))

        # Verify body
        # TODO: DRY
        body_signature = {}
        for key in body['required']:
            item = None
            if key not in kwargs:
                if 'default' not in body['data'][key]:
                    raise SyntaxError(f'Body key {key!r} is a required keyword argument')
                else:
                    item = body['data'][key]['default']

            if not item:
                item = kwargs[key]

            if 'validator' in body['data'][key]:
                tested = body['data'][key]['validator'](item)
                if not tested:
                    # TODO: less generic error messages by abstracting this to the endpoint data structure
                    raise ValueError(f'Supplied argument {key!r} failed to validate')

            body_signature[key] = item if method_info['body_type'] == 'json' else \
                format_parameter(item)

        for key in body['optional']:
            if key in kwargs:
                if 'validator' in body['data'][key]:
                    tested = body['data'][key]['validator'](kwargs[key])
                    if not tested:
                        # TODO: less generic error messages by abstracting this to the endpoint data structure
                        raise ValueError(f'Supplied argument {key!r} failed to validate')

                body_signature[key] = kwargs[key] if method_info['body_type'] == 'json' else \
                    format_parameter(kwargs[key])

        if method_info['http_method'] in ['POST', 'PUT', 'PATCH']:
            # Have a body
            if method_info['body_type'] == 'kv':
                resp = await self.signed_request(
                    method_info['http_method'], endpoint, params=params_signature, data=body_signature,
                    headers={'content-type': method_info['content_type']}
                )
            elif method_info['body_type'] == 'json':
                resp = await self.signed_request(
                    method_info['http_method'], endpoint, params=params_signature, json=body_signature,
                    headers={'content-type': method_info['content_type']}
                )
            else:
                raise RuntimeError(
                    f'Unknown body type {method_info["body_type"]!r} in method {method_info["method_name"]!r}'
                )
        elif method_info['http_method'] in ['GET', 'DELETE']:
            # No body for these methods, nor a specific content-type
            resp = await self.signed_request(
                method_info['http_method'], endpoint, params=params_signature
            )
        else:
            raise NotImplementedError(
                f'Unsupported HTTP verb {method_info["http_method"]!r}.'
            )

        return resp

    inner_method.__doc__ = generate_docstring(params, body, method_info)
    setattr(client, method_info['method_name'], inner_method)
