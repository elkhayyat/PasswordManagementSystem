from abc import ABC, abstractmethod


class BaseRepository(ABC):
    def __init__(self):
        self.run()

    def prepare(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def run(self):
        self.prepare()
        self.execute()
