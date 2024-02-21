from __future__ import annotations

from typing import (
    Any,
)
from unittest import (
    IsolatedAsyncioTestCase,
)
from unittest.mock import (
    MagicMock,
)

from enjo_lib.comm.internal import (
    InternalExchanger,
    InternalTransport,
)


# adapted from https://stackoverflow.com/a/32498408
class AsyncCallableMock(MagicMock):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return super().__call__(*args, **kwargs)


class InternalTransportTwoPeers(IsolatedAsyncioTestCase):

    async def test_simple_two_peers(self) -> None:
        # TODO move much stuff to setup methods
        exchange = InternalExchanger()
        # setup peers
        peer_alice = InternalTransport()
        exchange.register_transport(peer_alice)
        peer_bob = InternalTransport()
        exchange.register_transport(peer_bob)
        # setup mock receiving services
        mock_alice = AsyncCallableMock()
        peer_alice.on_receive(mock_alice)
        mock_bob = AsyncCallableMock()
        peer_bob.on_receive(mock_bob)
        # send from Alice to Bob
        await peer_alice.send("test Alice -> Bob")
        mock_alice.assert_not_called()
        mock_bob.assert_called_once_with("test Alice -> Bob")
        mock_alice.reset_mock()
        mock_bob.reset_mock()
        # send from Bob to Alice
        await peer_bob.send("test Bob -> Alice")
        mock_alice.assert_called_once_with("test Bob -> Alice")
        mock_bob.assert_not_called()
