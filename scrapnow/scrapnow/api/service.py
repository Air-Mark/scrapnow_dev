from .views import (
    ScrapperAddTaskView,
    ArticleRetrieveView
)
from ..db import ScrapnowDatabase
from ..lib.http import HTTPServer, Routes as BaseRoutes
from ..lib.service import Service as BaseService


class Routes(BaseRoutes):
    _routes = [
        ('*', '/scrapper/add_task', ScrapperAddTaskView),
        ('*', '/article/retrieve', ArticleRetrieveView)
    ]


class Service(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = ScrapnowDatabase(self, 'scrapnow_db')
        self.http_server = HTTPServer(self, 'web_server')
        self.routes = Routes(self, 'routes', self.http_server)

    async def start(self):
        return await super().start()
