from collections import AsyncIterable

from asyncpgsa import PG
from sqlalchemy import select

from scrapnow.lib.component import Component
from .schema import (
    scrap_task,
    scrap_document_fields,
    article,
    TaskStatus
)


class QueryAsyncIterable(AsyncIterable):
    PREFETCH = 100

    def __init__(self, query, transaction_context):
        self.query = query
        self.transaction_ctx = transaction_context

    async def __aiter__(self):
        async with self.transaction_ctx as conn:
            cursor = conn.cursor(self.query, prefetch=self.PREFETCH)
            async for row in cursor:
                yield row


class ScrapnowDatabase(Component, PG):

    async def start(self):
        self.log.info('Connecting to database')
        await self.init(**self.cfg)
        self.log.info('Connected to database')

    async def stop(self):
        self.log.info('Disconnecting from database')
        await self.pool.close()
        self.log.info('Disconnected from database')

    async def get_pending_scrap_tasks(self, count):
        tasks = None

        async with self.transaction() as connection:
            _tasks = await connection.fetch(
                select([scrap_task]).where(
                    scrap_task.c.status == TaskStatus.PENDING.value
                ).limit(count).with_for_update(key_share=True)
            )
            tasks = {task['id']: dict(task) for task in _tasks}
            if tasks:
                task_ids = list(tasks.keys())
                await connection.fetchrow(
                    scrap_task.update().values(
                        status=TaskStatus.IN_PROGRESS.value
                    ).where(scrap_task.c.id.in_(task_ids))
                )
                fields = await connection.fetch(
                    select([scrap_document_fields]).where(
                        scrap_document_fields.c.scrap_task_id.in_(task_ids)
                    )
                )
                for field in fields:
                    tasks[field['scrap_task_id']].setdefault(
                        'scrap_document_fields', []
                    ).append(field)

        return tasks

    async def add_scrap_task(self, url, document_fields, handler=None):
        async with self.transaction() as connection:
            task = await connection.fetchrow(
                scrap_task.insert().values(url=url, handler=handler).returning(
                    scrap_task.c.id)
            )
            if document_fields:
                for field in document_fields:
                    await connection.fetchrow(
                        scrap_document_fields.insert().values(
                            scrap_task_id=task['id'],
                            name=field['name'],
                            xpath=field['xpath']
                        ).returning(scrap_document_fields.c.id)
                    )

        await self.fetchrow("SELECT pg_notify('scrapnow', '');")

        return task['id']

    async def update_task(self, task_id, **values):
        if values.get('error'):
            status = TaskStatus.ERROR.value
        else:
            status = TaskStatus.ERROR.value

        await self.fetchrow(scrap_task.update().values(
            status=status,
            **values
        ).where(scrap_task.c.id == task_id))

    async def create_article(self, **values):
        article_id = await self.fetchrow(
            article.insert().values(**values).returning(article.c.id)
        )
        return article_id

    async def update_article(self, url, **values):
        await self.fetchrow(article.update().values(
            **values
        ).where(article.c.url == url))

    async def get_articles(self, datetime):
        query = select([article]).where(article.c.datetime == datetime)
        # query = select([article])
        return QueryAsyncIterable(query, self.transaction())
