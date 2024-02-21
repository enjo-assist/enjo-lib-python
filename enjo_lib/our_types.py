from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from decimal import (
    Decimal,
)
from typing import (
    TypeAlias,
    Union,
)


JSON: TypeAlias = Union[
    Mapping[str, "JSON"],
    Sequence["JSON"],
    str,
    int,
    Decimal,
    bool,
]
