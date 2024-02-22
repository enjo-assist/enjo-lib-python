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

from ...our_types import (
    JSON,
)


class TransmissionSuccess(Enum):
    UNKNOWN_ERROR = auto()
    EXCHANGE_UNAVAILABLE = auto()
    SUBMITTED_SUCCESSFULLY = auto()


MessageHandler: TypeAlias = Callable[[JSON], Awaitable[None]]


class TransportMethod(ABC):

    @abstractmethod
    async def send(self, data: JSON) -> TransmissionSuccess: ...

    @abstractmethod
    def on_receive(self, handler: MessageHandler) -> None:
        """sets the handler, there can only be one set"""
        ...
