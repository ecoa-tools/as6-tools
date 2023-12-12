# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.ecoa.technology/bin-desc-2.0"


class ProgrammingLanguage(Enum):
    """Programming languages supported by ECOA bindings.

    :cvar C:
    :cvar C_1:
    :cvar ADA:
    :cvar JAVA:
    :cvar HI_ADA:
    """

    C = "C"
    C_1 = "C++"
    ADA = "Ada"
    JAVA = "Java"
    HI_ADA = "HI_Ada"


@dataclass
class Use:
    """Declares the use of a library of data types. A type T defined in a library L
    will be denoted "L:T".

    :ivar library:
    """

    class Meta:
        name = "use"
        namespace = "http://www.ecoa.technology/bin-desc-2.0"

    library: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute", required=True, pattern=r"[A-Za-z][A-Za-z0-9_\.]*"),
    )
