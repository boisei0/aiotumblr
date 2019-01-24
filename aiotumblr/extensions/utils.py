# encoding=utf-8
from typing import Dict, Any, Tuple, Union

import forge


def format_docstring_for_sphinx(docstring: str, indent: int = 3) -> str:
    lines = docstring.split('\n')
    lines_new = []
    for line in lines:
        lines_new.append(f"{indent * ' '}{line}") if len(line.strip()) > 0 else lines_new.append('')
    return '\n'.join(lines_new)


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
    ds_url_params = '\n'.join(f""":param {key}: {url_param['description']}
:type {key}: {url_param['type'].__name__}""" for key, url_param in method_info['url_parameters'].items())

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

    ds = f"""{method_info['description_summary']}\n"""

    if method_info['description_long']:
        ds += f"""\n{method_info['description_long']}\n"""

    if ds_url_params:
        ds += f"""\n{ds_url_params}"""

    if ds_required_params:
        ds += f"""\n{ds_required_params}"""

    if ds_optional_params:
        ds += f"""\n{ds_optional_params}"""

    if ds_required_body_args:
        ds += f"""\n{ds_required_body_args}"""

    if ds_optional_body_args:
        ds += f"""\n{ds_optional_body_args}"""

    ds += f"""\n:return: API response for {method_info['method_name']}
:rtype: `aiohttp.ClientResponse`
:raises SyntaxError: if required parameter is missing
:raises ValueError: if supplied parameter fails validation
"""

    return ds


def create_method(client, params, body, method_info):
    _sig_url_params = []
    _sig_params_req = []
    _sig_params_opt = []
    _sig_body_req = []
    _sig_body_opt = []

    for _key, _url_param in method_info['url_parameters'].items():
        _sig_url_params.append(forge.arg(name=_key, type=_url_param['type']))

    if params['data']:
        for _key, _param_item in params['data'].items():
            if _param_item['required']:
                _sig_params_req.append(forge.arg(name=_key, type=_param_item['type']))
            else:
                _sig_params_opt.append(forge.kwo(name=_key, type=_param_item['type'], default=None))

    if body['data']:
        for _key, _body_item in body['data'].items():
            if _body_item['required']:
                _sig_body_req.append(forge.arg(name=_key, type=_body_item['type']))
            else:
                _sig_body_opt.append(forge.kwo(name=_key, type=_body_item['type'], default=None))

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
            if param in kwargs and kwargs[param] is not None:
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
            if key in kwargs and kwargs[key] is not None:
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

    revised = forge.sign(
        forge.pos(name='self'),
        *_sig_url_params,
        *_sig_params_req,
        *_sig_body_req,
        *_sig_params_opt,
        *_sig_body_opt,
    )(inner_method)
    revised.__name__ = method_info['method_name']

    revised.__doc__ = generate_docstring(params, body, method_info)
    setattr(client, method_info['method_name'], revised)
