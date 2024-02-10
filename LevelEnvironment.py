from abc import ABC, abstractmethod
import pygame


class IDrawAble(ABC):
    @abstractmethod
    def draw(self):
        ...


class Food(IDrawAble):
    def draw(self):
        pass


class Energiser(IDrawAble):
    def draw(self):
        pass


class Wall(IDrawAble):
    def draw(self):
        pass


class CurvedWall(IDrawAble):
    def draw(self):
        pass
