from abc import ABC, abstractmethod


# create abstract base class which enforces driver classes to perform given task
class AbstractDriver(ABC):

    def __init__(self, config):
        self.config = config
        # self.workload = generate_workload(
        #     config.get('workload', 'WORKLOAD_TYPE'),
        #     config.get('workload', 'WORKLOAD_SIZE')
        # )

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def handle_workload(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass



