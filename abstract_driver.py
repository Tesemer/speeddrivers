from abc import ABC, abstractmethod


# create abstract base class which enforces driver classes to perform given task
class AbstractDriver(ABC):

    def __init__(self, config, workload):
        self.config = config
        self.workload = workload

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def handle_workload(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass



