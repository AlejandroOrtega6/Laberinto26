from __future__ import annotations
from abc import ABC, abstractmethod

class EstadoEnte(ABC):

    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def esta_vivo(self) -> bool:
        pass

class Vivo(EstadoEnte):

    def nombre(self) -> str:
        return 'vivo'

    def esta_vivo(self) -> bool:
        return True

class Muerto(EstadoEnte):

    def nombre(self) -> str:
        return 'muerto'

    def esta_vivo(self) -> bool:
        return False
