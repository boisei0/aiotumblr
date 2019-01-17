# encoding=utf-8
def format_parameter(param):
    if isinstance(param, bool):
        return str(param).lower()
    return param


def create_method(client, params, body, method_info):
    async def inner_method(self, **kwargs):
        # Verify signature
        endpoint_signature = {}
        for url_param in method_info['url_parameters']:
            if url_param not in kwargs:
                raise RuntimeError(f'Argument {url_param!r} is a required keyword argument.')
            endpoint_signature[url_param] = kwargs[url_param]
        endpoint = method_info['endpoint'].format(**endpoint_signature)

        # Verify params
        # TODO: Add validator check
        params_signature = []
        for param in params['required']:
            if param not in kwargs:
                raise RuntimeError(f'Parameter {param!r} is a required keyword argument')
            params_signature.append((param, format_parameter(kwargs[param])))
        for param in params['optional']:
            if param in kwargs:
                params_signature.append((param, format_parameter(kwargs[param])))

        # Verify body
        # TODO: Add validator check
        body_signature = {}
        for key in body['required']:
            if key not in kwargs:
                raise RuntimeError(f'Body key {key!r} is a required keyword argument')
            body_signature[key] = kwargs[key] if method_info['body_type'] == 'json' else \
                format_parameter(kwargs[key])
        for key in body['optional']:
            if key in kwargs:
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

    # TODO: Dynamically generate docstring
    setattr(client, method_info['method_name'], inner_method)
