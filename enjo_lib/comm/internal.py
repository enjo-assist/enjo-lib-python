from __future__ import annotations

import asyncio
from functools import partial

from .method import (
    MessageHandler,
    TransportMethod,
    TransmissionSuccess,
)
from ..our_types import JSON


class InternalTransport(TransportMethod):
    """transport method for multiple enjo services running together in the same Python thread.
    built for asyncio, not for communicating across multiple threads.

    create one for each service"""

    __recv_handler: MessageHandler | None = None
    __send_handler: MessageHandler | None = None

    async def send(self, data: JSON) -> TransmissionSuccess:
        if self.__send_handler is None:
            return TransmissionSuccess.EXCHANGE_UNAVAILABLE
        await self.__send_handler(data)
        return TransmissionSuccess.SUBMITTED_SUCCESSFULLY

    def on_receive(self, handler: MessageHandler) -> None:
        self.__recv_handler = handler

    async def _submit(self, data: JSON) -> None:
        if self.__recv_handler is None:
            return
        await self.__recv_handler(data)

    def _on_send(self, handler: MessageHandler) -> None:
        self.__send_handler = handler


class InternalExchanger:

    __transports = set[InternalTransport]()

    async def __send_handler(self, sender: InternalTransport, data: JSON) -> None:
        async with asyncio.TaskGroup() as group:
            for receiver in self.__transports:
                if receiver is sender:
                    continue
                group.create_task(receiver._submit(data))

    def register_transport(self, transport: InternalTransport) -> None:
        if transport in self.__transports:
            return
        self.__transports.add(transport)
        transport._on_send(partial(self.__send_handler, transport))
