import asyncio

import aiohttp
from lxml import html as lxml_html

from .handlers.basic import BasicHandler
from .handlers.reuters_article import ReutersArticleTaskHandler
from ..db import ScrapnowDatabase
from ..db.listener import DBListener
from ..db.schema import TaskHandlers
from ..lib.service import Service as BaseService


class Service(BaseService):
    TASK_PER_WORKER = 10
    handler_classes = {
        None: BasicHandler,
        TaskHandlers.REUTERS_ARTICLE.value: ReutersArticleTaskHandler
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = ScrapnowDatabase(self, 'scrapnow_db')
        self.listener = DBListener(
            self,
            'scrapnow_listener',
            'scrapnow',
            self.check_new_tasks
        )

    async def start(self):
        await super().start()
        await self.check_new_tasks()

    async def check_new_tasks(self, *args, **kwargs):
        while True:
            tasks = await self.db.get_pending_scrap_tasks(self.TASK_PER_WORKER)

            if not tasks:
                break
            await asyncio.gather(*[self.scrap(task_id, task)
                                   for task_id, task in tasks.items()])

    async def _fetch_html(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()
                html = lxml_html.fromstring(data)
        return html

    def handler_factory(self, task, html_dom):
        handler_cls = self.handler_classes.get(task.get('handler'))
        if handler_cls:
            return handler_cls(self, task, html_dom)
        return None

    async def scrap(self, task_id, task):
        try:
            html_dom = await self._fetch_html(task['url'])
            if html_dom and len(html_dom):

                task_handler = self.handler_factory(task, html_dom)
                if task_handler:
                    await task_handler.run()

        except Exception as exp:
            self.log.exception('Scrap task failed')
            await self.db.update_task(task_id, error=repr(exp))
