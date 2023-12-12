# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/interface-2.0"


@dataclass
class Data:
    """Use of the "versioned data" exchange mechanism.

    :ivar name:
    :ivar comment:
    :ivar type:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field(default=None, metadata=dict(type="Attribute"))
    type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


class EEventDirection(Enum):
    """
    :cvar SENT_BY_PROVIDER:
    :cvar RECEIVED_BY_PROVIDER:
    """

    SENT_BY_PROVIDER = "SENT_BY_PROVIDER"
    RECEIVED_BY_PROVIDER = "RECEIVED_BY_PROVIDER"


@dataclass
class Parameter:
    """
    :ivar name:
    :ivar type:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class Event:
    """Use of the "event" exchange mechanism.

    :ivar name:
    :ivar comment:
    :ivar input:
    :ivar direction:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field(default=None, metadata=dict(type="Attribute"))
    input: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    direction: Optional[EEventDirection] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class RequestResponse:
    """Use of the "request-response" exchange mechanism.

    :ivar name:
    :ivar comment:
    :ivar input:
    :ivar output:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field(default=None, metadata=dict(type="Attribute"))
    input: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    output: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class Operations:
    """A set of named operations.

    :ivar data:
    :ivar event:
    :ivar requestresponse:
    """

    data: List[Data] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    event: List[Event] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    requestresponse: List[RequestResponse] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class ServiceDefinition:
    """The definition of an ECOA service, including a set of operations.

    :ivar use:
    :ivar operations:
    """

    use: List[str] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    operations: Optional[Operations] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-2.0",
            required=True,
        ),
    )


@dataclass
class ServiceDefinition(ServiceDefinition):
    class Meta:
        name = "serviceDefinition"
        namespace = "http://www.ecoa.technology/interface-2.0"
