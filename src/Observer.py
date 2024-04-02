from abc import ABC, abstractmethod


class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.update_observer(event)


class IObserver(ABC):
    @abstractmethod
    def update_observer(self, event):
        pass
