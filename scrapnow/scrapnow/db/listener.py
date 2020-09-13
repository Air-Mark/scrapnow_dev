import asyncio

import asyncpg

from ..lib.component import Component


class DBListener(Component):
    channel = 'scrapnow'

    def __init__(self, service, name, channel, callback):
        super().__init__(service, name)
        self.conn = None
        self.channel = channel
        self.callback = callback

    async def start(self):
        self.conn = await asyncpg.connect(**self.cfg)
        await self.conn.add_listener(self.channel, self._callback)

    async def stop(self):
        if self.conn:
            await self.conn.remove_listener(self.channel, self._callback)
            await self.conn.close()

    def _callback(self, conn, pid, channel, payload):
        asyncio.create_task(self.callback(payload))
