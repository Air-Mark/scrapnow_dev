LIST_ITEM_XPATH = "//div[@id='bodyblock']/ul/li[@class='regularitem']"


class BasicHandler:

    def __init__(self, service, task, html_dom):
        self.service = service
        self.task = task
        self.html_dom = html_dom

    async def run(self):
        result = await self.process_task()
        await self.finish_task(result)

    async def process_task(self):
        result = {}

        if 'scrap_document_fields' in self.task:
            for field in self.task['scrap_document_fields']:
                field_data = self.html_dom.xpath(field['xpath'])
                result[field['name']] = field_data

        return result

    async def finish_task(self, result):
        await self.service.db.update_task(self.task['id'], result=result)
