from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import (
    Literal,
    Type,
)

from attrs import (
    define,
)

from ...our_types import (
    EpochId,
    HumanFriendlyDesc,
    InstanceId,
    JSON,
    ServiceType,
    ServiceClass,
)


@define(
    frozen=True,
    kw_only=True,
)
class GeneralTransportDatagram:
    _version: int = 1
    timestamp_ns: int
    sender: InstanceId
    message_type: str
    data: JSON | GeneralTransportMetadata | None


@define(
    frozen=True,
    kw_only=True,
)
class GeneralTransportMetadata:
    pass


# connect


@define(
    frozen=True,
    kw_only=True,
)
class ConnectDatagram(GeneralTransportDatagram):
    message_type: Literal["connect"] = "connect"
    data: ConnectMetadata


@define(
    frozen=True,
    kw_only=True,
)
class ConnectMetadata(GeneralTransportMetadata):
    epoch: EpochId
    type: ServiceType
    service_classes: Sequence[ServiceClass]


# disconnect


@define(
    frozen=True,
    kw_only=True,
)
class DisconnectDatagram(GeneralTransportDatagram):
    message_type: Literal["disconnect"] = "disconnect"
    data: DisconnectMetadata


@define(
    frozen=True,
    kw_only=True,
)
class DisconnectMetadata(GeneralTransportMetadata):
    epoch: EpochId
    exceptional: bool
    reason: HumanFriendlyDesc


# duplicate & replace sender types


@define(
    frozen=True,
    kw_only=True,
)
class DuplicateSenderDatagram(GeneralTransportDatagram):
    message_type: Literal["duplicate_sender"] = "duplicate_sender"
    data: ConnectMetadata


@define(
    frozen=True,
    kw_only=True,
)
class ReplaceSenderDatagram(GeneralTransportMetadata):
    message_type: Literal["replace_sender"] = "replace_sender"
    data: ConnectMetadata


# failure


@define(
    frozen=True,
    kw_only=True,
)
class FailureDatagram(GeneralTransportDatagram):
    message_type: Literal["failure"] = "failure"
    data: FailureMetadata


@define(
    frozen=True,
    kw_only=True,
)
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


@define(
    frozen=True,
    kw_only=True,
)
class RestartDatagram(GeneralTransportDatagram):
    """issues a restart of a whole Enjo network"""

    message_type: Literal["restart"] = "restart"
    data: None = None


# transmit


@define(
    frozen=True,
    kw_only=True,
)
class TransmitDatagram(GeneralTransportDatagram):
    message_type: Literal["transmit"] = "transmit"
    data: JSON


MESSAGE_TYPE_MAP: Mapping[str, Type[GeneralTransportDatagram]] = {
    "connect": ConnectDatagram,
    "disconnect": DisconnectDatagram,
    "duplicate_sender": DuplicateSenderDatagram,
    "replace_sender": ReplaceSenderDatagram,
    "failure": FailureDatagram,
    "restart": RestartDatagram,
    "transmit": TransmitDatagram,
}
