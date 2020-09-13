from aiohttp import web
from aiohttp_apispec import (
    response_schema,
    querystring_schema,
    json_schema
)

from .schema import (
    ArticleFindNewRequest,
    ApiResponse,
    ScrapperAddTaskRequest,
    ArticleRetrieveRequest,
    ArticleRetrieveResponse,
)
from ..lib.http import HTTPView


class BaseApiView(HTTPView):

    async def _iter(self):
        result = await super()._iter()
        if isinstance(result, web.Response):
            return result
        else:
            handler = getattr(
                self.request.match_info.handler,
                self.request.method.lower()
            )
            schema = handler.__apispec__['responses']['200']['schema']
            return web.json_response(schema.dump(result))


class ScrapperAddTaskView(BaseApiView):

    @property
    def url(self):
        return self.request['json']['url']

    @property
    def document_fields(self):
        return self.request['json'].get('document_fields')

    @property
    def handler(self):
        return self.request['json'].get('handler')

    @json_schema(ScrapperAddTaskRequest)
    @response_schema(ApiResponse)
    async def post(self):
        await self.service.db.add_scrap_task(
            self.url,
            self.document_fields,
            self.handler
        )
        return {}


class ArticleFindNewView(BaseApiView):

    @querystring_schema(ArticleFindNewRequest)
    @response_schema(ApiResponse)
    async def get(self):
        return {}


class ArticleRetrieveView(BaseApiView):

    @querystring_schema(ArticleRetrieveRequest)
    @response_schema(ArticleRetrieveResponse)
    async def get(self):
        datetime = self.request['querystring']['date']
        datetime = datetime.replace(tzinfo=None)
        data = await self.service.db.get_articles(datetime)
        return web.Response(body=data)
