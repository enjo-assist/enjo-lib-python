from __future__ import annotations

from collections.abc import (
    Sequence,
)
from typing import (
    Literal,
)

from ...our_types import (
    EpochId,
    HumanFriendlyDesc,
    InstanceId,
    JSON,
    ServiceType,
    ServiceClass,
    serializable,
)


@serializable
class GeneralTransportDatagram:
    _version: int = 1
    timestamp_ns: int
    sender: InstanceId
    message_type: str
    data: JSON | GeneralTransportMetadata | None


@serializable
class GeneralTransportMetadata:
    pass


# connect


@serializable
class ConnectDatagram(GeneralTransportDatagram):
    message_type: Literal["connect"] = "connect"
    data: ConnectMetadata


@serializable
class ConnectMetadata(GeneralTransportMetadata):
    epoch: EpochId
    type: ServiceType
    service_classes: Sequence[ServiceClass]


# disconnect


@serializable
class DisconnectDatagram(GeneralTransportDatagram):
    message_type: Literal["disconnect"] = "disconnect"
    data: DisconnectMetadata


@serializable
class DisconnectMetadata(GeneralTransportMetadata):
    epoch: EpochId
    exceptional: bool
    reason: HumanFriendlyDesc


# duplicate & replace sender types


@serializable
class DuplicateSenderDatagram(GeneralTransportDatagram):
    message_type: Literal["duplicate_sender"] = "duplicate_sender"
    data: ConnectMetadata


@serializable
class ReplaceSenderDatagram(GeneralTransportMetadata):
    message_type: Literal["replace_sender"] = "replace_sender"
    data: ConnectMetadata


# failure


@serializable
class FailureDatagram(GeneralTransportDatagram):
    message_type: Literal["failure"] = "failure"
    data: FailureMetadata


@serializable
class FailureMetadata(GeneralTransportMetadata):
    """
    Issues that a specific service has failed.

    This does not mean that the whole stack might be failed as each service may run on its own.
    But most certainly, if the controller does issue an failure, it likely is the whole stack.
    """

    epoch: EpochId
    reason: HumanFriendlyDesc
    debug_data: JSON


# restart


@serializable
class RestartDatagram(GeneralTransportDatagram):
    """issues a restart of a whole Enjo network"""

    message_type: Literal["restart"] = "restart"
    data: None = None


# transmit


@serializable
class TransmitDatagram(GeneralTransportDatagram):
    message_type: Literal["transmit"] = "transmit"
    data: JSON
