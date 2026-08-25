from dataclasses import dataclass

from model.artObject import artObject


@dataclass
class Arco:
    o1: artObject
    o2: artObject
    peso: int