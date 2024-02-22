from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    Enum,
    auto,
)
from typing import (
    Awaitable,
    Callable,
    TypeAlias,
)


class TransmissionSuccess(Enum):
    UNKNOWN_ERROR = auto()
    EXCHANGE_UNAVAILABLE = auto()
    SUBMITTED_SUCCESSFULLY = auto()


MessageHandler: TypeAlias = Callable[[bytes], Awaitable[None]]


class TransportMethod(ABC):

    @abstractmethod
    async def send(self, data: bytes) -> TransmissionSuccess: ...

    @abstractmethod
    def on_receive(self, handler: MessageHandler) -> None:
        """sets the handler, there can only be one set"""
        ...
