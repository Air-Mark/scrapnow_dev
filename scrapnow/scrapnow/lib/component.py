from logging import getLogger

from .service import Service


class Component:
    def __init__(self, service: Service, name: str) -> None:
        self.service = service
        self.name = name
        self.qname = '.'.join([self.service.name, self.name])
        self.log = getLogger(name)
        service.register_component(self)

    @property
    def cfg(self):
        return self.service.cfg[self.name]

    async def start(self):
        pass

    async def stop(self):
        pass


class SubComponent(Component):

    def __init__(self, service: Service,
                 name: str,
                 parent_component: Component):
        super().__init__(service, name)
        self.parent_component = parent_component
