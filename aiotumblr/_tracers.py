import logging

from aiohttp.tracing import TraceConfig, TraceRequestStartParams, TraceRequestEndParams, TraceRequestRedirectParams


class AIOTumblrDebugger(TraceConfig):
    def __init__(self, logger: logging.Logger):
        super().__init__()

        self._log = logger

        self.on_request_start.append(self._on_request_start_handler)
        self.on_request_end.append(self._on_request_end_handler)
        self.on_request_redirect.append(self._on_request_redirection_handler)

    async def _on_request_start_handler(self, session, ctx, params: TraceRequestStartParams):
        self._log.debug(f'Starting {params.method} request to {params.url.human_repr()}')
        self._log.debug(f'With headers: {params.headers}')

    async def _on_request_end_handler(self, session, ctx, params: TraceRequestEndParams):
        self._log.debug(f'Ending {params.method} request to {params.url.human_repr()}')
        self._log.debug(f'With headers: {params.headers}')

    async def _on_request_redirection_handler(self, session, ctx, params: TraceRequestRedirectParams):
        self._log.debug(f'Redirecting to {params.method} {params.url.human_repr()}')
        self._log.debug(f'With headers: {params.headers}')
