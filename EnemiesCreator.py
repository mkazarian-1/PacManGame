from abc import ABC, abstractmethod


class Ghost(ABC):
    @abstractmethod
    def move(self):
        ...


class RedGhost(Ghost):
    def move(self):
        pass


class BlueGhost(Ghost):
    def move(self):
        pass


class OrangeGhost(Ghost):
    def move(self):
        pass


class PinkGhost(Ghost):
    def move(self):
        pass
