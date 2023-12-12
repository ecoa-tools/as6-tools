# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/uid-2.0"


@dataclass
class Id:
    """
    :ivar key:
    :ivar value:
    """

    class Meta:
        name = "ID"

    key: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    value: Optional[int] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class IdMap:
    """
    :ivar id:
    """

    class Meta:
        name = "ID_map"
        namespace = "http://www.ecoa.technology/uid-2.0"

    id: List[Id] = field(
        default_factory=list,
        metadata=dict(name="ID", type="Element", min_occurs=0, max_occurs=9223372036854775807),
    )
