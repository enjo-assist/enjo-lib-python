from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import (
    TypeAlias,
    NewType,
    Union,
)
from uuid import (
    UUID,
)


JSON: TypeAlias = Union[
    Mapping[str, "JSON"],
    Sequence["JSON"],
    str,
    int,
    float,
    bool,
]


ReverseDomainArg = NewType("ReverseDomainArg", str)
"""e.g. `"de.6nw.enjo.controller"`"""


InstanceId = NewType("InstanceId", UUID)
ServiceType = NewType("ServiceType", ReverseDomainArg)
ServiceClass = NewType("ServiceClass", ReverseDomainArg)
EpochId = NewType("EpochId", UUID)
HumanFriendlyDesc = NewType("HumanFriendlyDesc", str)
