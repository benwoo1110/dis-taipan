"""
Sets up a Sentry Logger
"""
from typing import Any
import logging
from dis_snek import Snake, Scale, listen
import sentry_sdk
import os

def sentry_filter(event: dict[str, Any], hint: dict[str, Any]):  # type: ignore
    if 'log_record' in hint:
        record: logging.LogRecord = hint['log_record']
        if 'dis.snek' in record.name:
            if '/commands/permissions: 403' in record.message:
                return None
            if record.message.startswith('Ignoring exception in '):
                return None

    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, OSError):
            return None
    return event

_default_error_handler = Snake.default_error_handler

class SentryScale(Scale):
    @listen()
    async def on_startup(self) -> None:
        sentry_sdk.set_context('bot', {
            'name': str(self.bot.user),
            'intents': repr(self.bot.intents),
        })

    def default_error_handler(self, source: str, error: Exception) -> None:
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('source', source)
            sentry_sdk.capture_exception(error)
        _default_error_handler(source, error)

    Snake.default_error_handler = default_error_handler

def setup(bot: Snake) -> None:
    token = os.environ.get('SENTRY_TOKEN')
    if not token:
        logging.error('Sentry token not found, disabling sentry')
    sentry_sdk.init(token, before_send=sentry_filter)
    SentryScale(bot)
