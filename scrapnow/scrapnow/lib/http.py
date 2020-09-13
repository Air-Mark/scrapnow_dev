import json
from datetime import datetime
from functools import partial, singledispatch
from http import HTTPStatus
from types import AsyncGeneratorType
from typing import AsyncIterable
from urllib.parse import urlparse

import aiohttp.web
from aiohttp import PAYLOAD_REGISTRY
from aiohttp.payload import Payload
from aiohttp.web_exceptions import (
    HTTPBadRequest, HTTPException, HTTPInternalServerError
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from asyncpg import Record
from marshmallow import ValidationError

from .component import Component, SubComponent
from .service import Service


class HTTPServer(Component):

    @property
    def uri(self):
        return '{}://{}:{}{}'.format(
            self.url.scheme,
            self.url.hostname,
            self.url.port,
            self.url.path
        )

    @middleware
    async def error_middleware(self, request, handler):
        def _error(error_cls, message=None):
            status = HTTPStatus(error_cls.status_code)

            if message:
                try:
                    message = json.loads(message)
                except (TypeError, json.JSONDecodeError):
                    pass

            error = {
                'code': status.name.lower(),
                'message': message or status.description
            }

            return error_cls(body=json.dumps({'error': error}),
                             content_type='application/json')

        try:
            return await handler(request)
        except HTTPException as err:
            raise _error(err.__class__, err.text)
        except ValidationError as err:
            raise _error(HTTPBadRequest, {err.field_name: err.messages})
        except Exception:
            self.log.exception('Something went wrong')
            raise _error(HTTPInternalServerError)

    def __init__(self, service, name):
        super(HTTPServer, self).__init__(service, name)
        self.url = urlparse(self.cfg.get('url'))
        self.web_application = aiohttp.web.Application(
            middlewares=[self.error_middleware, validation_middleware]
        )
        self.server = None
        self.handler = None

    async def start(self):
        self.handler = self.web_application.make_handler(keepalive_timeout=15)
        self.server = await self.service.loop.create_server(
            self.handler,
            self.url.hostname,
            self.url.port
        )

    def add_route(self, method, path, handler):
        self.log.info(
            'ADD: %6s %s%s %s', method, self.uri, path, handler
        )
        self.web_application.router.add_route(method, path, handler)


class HTTPView(aiohttp.web.View):
    component = None

    @classmethod
    def set_component(cls, component):
        cls.component = component

    @property
    def cfg(self):
        return self.component.cfg

    @property
    def service(self):
        return self.component.service


class Routes(SubComponent):
    _routes = []

    def __init__(self, service: Service, name: str, component: HTTPServer):
        super().__init__(service, name, component)
        for method, path, view in self._routes:
            if issubclass(view, HTTPView):
                view.set_component(self)
                self.parent_component.add_route(method, path, view)
            else:
                self.log.error('%s is not subclass of HTTPView', view)

        swagger_path = '/doc'

        setup_aiohttp_apispec(
            app=self.parent_component.web_application,
            title=f"{self.service.name} documentation",
            swagger_path=swagger_path,
            in_place=True
        )
        self.log.info(
            'DOCUMENTATION: %s%s', self.parent_component.uri, swagger_path
        )


@singledispatch
def convert(value):
    raise TypeError(f'Unserializable value: {value!r}')


@convert.register(Record)
def convert_asyncpg_record(value: Record):
    return dict(value)


@convert.register(datetime)
def convert_date(value):
    return value.timestamp()


dumps = partial(json.dumps, default=convert, ensure_ascii=False)


class AsyncGenJSONListPayload(Payload):
    def __init__(self, value, encoding='utf-8',
                 content_type='application/json',
                 root_object='items',
                 *args, **kwargs):
        self.root_object = root_object
        super().__init__(value, content_type=content_type, encoding=encoding,
                         *args, **kwargs)

    async def write(self, writer):
        await writer.write(
            ('{"%s":[' % self.root_object).encode(self._encoding))
        first = True
        async for row in self._value:
            if not first:
                await writer.write(b',')
            else:
                first = False
            await writer.write(dumps(row).encode(self._encoding))
        await writer.write(b']}')


PAYLOAD_REGISTRY.register(AsyncGenJSONListPayload,
                          (AsyncGeneratorType, AsyncIterable))
