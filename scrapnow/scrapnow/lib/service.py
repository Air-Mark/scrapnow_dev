import asyncio
import logging


class Service:

    @staticmethod
    def get_event_loop():
        return asyncio.get_event_loop()

    def __init__(self, cfg, loop=None):
        self.cfg = cfg
        self.loop = loop or self.get_event_loop()
        self.name = self.cfg['service_name']
        self.log = logging.getLogger(self.name)
        self.log.info('CFG:')
        self.log.info(cfg)
        self.components = []

    @classmethod
    def proc_title(cls, cfg):
        return cfg['service_name']

    def register_component(self, component):
        self.components.append(component)

    async def start(self):
        for component in self.components:
            await component.start()

    async def stop(self):
        for component in reversed(self.components):
            await component.stop()
