import asyncio

import pendulum

from .basic import BasicHandler
from ...db.schema import ArticleStatus, TaskHandlers


class ReutersArticleTaskHandler(BasicHandler):
    BASE_URL = 'https://www.reuters.com/'
    LIST_PAGE_URL = 'https://www.reuters.com/news/archive/rates-rss'
    LIST_ITEM_XPATH = "//article[contains(@class,'story')]"
    LIST_ITEM_TITLE_XPATH = './/h3[@class="story-title"]/text()'
    LIST_ITEM_DESC_XPATH = './/p/text()'
    LIST_ITEM_DATE_XPATH = './/span[@class="timestamp"]/text()'
    LIST_ITEM_HREF_XPATH = './/div[@class="story-content"]/a/@href'
    ARTICLE_BODY_XPATH = "//div[@class='TwoColumnsLayout-body-86gsE ArticlePage-body-container-10RhS']//text()"  # noqa E501

    def __init__(self, service, task, html_dom):
        super().__init__(service, task, html_dom)

        self.html_dom.make_links_absolute(self.BASE_URL)

    async def process_task(self):
        if self._is_list_page():
            await self._process_list_page()
        else:
            await self._process_article_page()

        return None

    def _is_list_page(self):
        return self.task['url'] == self.LIST_PAGE_URL

    def _get_text(self, xpath, parent=None):
        parent = parent or self.html_dom
        elements = parent.xpath(xpath)
        if elements:
            return ' '.join(elements).strip()
        return None

    async def _process_list_page(self):
        article_thumbs = self.html_dom.xpath(self.LIST_ITEM_XPATH)
        for article in article_thumbs:
            title = self._get_text(self.LIST_ITEM_TITLE_XPATH, article)
            desc = self._get_text(self.LIST_ITEM_DESC_XPATH, article)
            href = self._get_text(self.LIST_ITEM_HREF_XPATH, article)

            date = self._get_text(self.LIST_ITEM_DATE_XPATH, article)
            if date:
                date = pendulum.from_format(date, 'MMM DD YYYY')
                date = date.replace(tzinfo=None)

            await asyncio.gather(
                self.service.db.create_article(
                    url=href,
                    title=title,
                    short_description=desc,
                    datetime=date
                ),
                self.service.db.add_scrap_task(
                    href,
                    document_fields=None,
                    handler=TaskHandlers.REUTERS_ARTICLE.value
                ), return_exceptions=True
            )

    async def _process_article_page(self):
        body = self._get_text(self.ARTICLE_BODY_XPATH)
        await self.service.db.update_article(
            self.task['url'],
            body=body,
            status=ArticleStatus.PROCESSED.value
        )
