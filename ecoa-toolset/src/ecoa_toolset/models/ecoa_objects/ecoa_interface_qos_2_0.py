# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/interface-qos-2.0"


@dataclass
class OperationRate:
    """
    :ivar number_of_occurrences: Min or max number of operations occurring
              during a specified duration
    :ivar time_frame: Equal to min or max inter-arrival time when
              NumberOfOccurrences value is 1.
              In other cases, specifies a sizing duration for operations
              bursts.
              Unit is second.
    """

    number_of_occurrences: Optional[Decimal] = field(
        default=None, metadata=dict(name="numberOfOccurrences", type="Attribute")
    )
    time_frame: Optional[str] = field(default=None, metadata=dict(name="timeFrame", type="Attribute"))


@dataclass
class Data:
    """Use of the "versionned data" exchange mechanism.

    :ivar highest_rate: Max number of occurrences within a
                reference time
                frame
    :ivar lowest_rate: Min number of occurrences within a
                reference time frame
    :ivar name:
    :ivar max_ageing: Operation Provided : max duration between
              Data production (from the source) and the end of writing
              process.
              Operation Required : max duration between Data
              production
              (from the source) and the end of reading process.
              Unit is second.
    :ivar notification_max_handling_time: Notifying data case: maxHandlingTime for
              notification event. Unit is second.
    """

    highest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="highestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    lowest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="lowestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    max_ageing: Optional[str] = field(default=None, metadata=dict(name="maxAgeing", type="Attribute"))
    notification_max_handling_time: Optional[str] = field(
        default=None,
        metadata=dict(name="notificationMaxHandlingTime", type="Attribute"),
    )


@dataclass
class Event:
    """Use of the "event" exchange mechanism.

    :ivar highest_rate: Max number of occurrences within a
                reference time frame
    :ivar lowest_rate: Min number of occurrences within a
                reference time frame
    :ivar name:
    :ivar max_handling_time: Event Sent : specifies an intent on receivers
              for maximal duration between Event Reception and end of
              related processing
              Event Received : maximal duration between
              Event Received and end of related processing.
              Unit is second.
    """

    highest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="highestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    lowest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="lowestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    max_handling_time: Optional[str] = field(default=None, metadata=dict(name="maxHandlingTime", type="Attribute"))


@dataclass
class RequestResponse:
    """Use of the "request-reply" exchange mechanism.

    :ivar highest_rate: Max number of occurrences within a
                reference time frame
    :ivar lowest_rate: Min number of occurrences within a
                reference time frame
    :ivar name:
    :ivar max_response_time: Operation Provided : maximal duration between
              Request Reception and Callback Sent
              Operation Required : maximal duration between Request Sent
              and Callback reception.
              Unit is second.
    :ivar callback_max_handling_time: maxHandlingTime to execute the callback
              entry-point.
              Unit is second.
    """

    highest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="highestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    lowest_rate: Optional[OperationRate] = field(
        default=None,
        metadata=dict(
            name="lowestRate",
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    max_response_time: Optional[str] = field(default=None, metadata=dict(name="maxResponseTime", type="Attribute"))
    callback_max_handling_time: Optional[str] = field(
        default=None, metadata=dict(name="callbackMaxHandlingTime", type="Attribute")
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
            namespace="http://www.ecoa.technology/interface-qos-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    event: List[Event] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    requestresponse: List[RequestResponse] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class ServiceInstanceQoS:
    """The definition of an ECOA service, including a set of operations.

    :ivar operations:
    """

    operations: Optional[Operations] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/interface-qos-2.0",
            required=True,
        ),
    )


@dataclass
class ServiceInstanceQoS(ServiceInstanceQoS):
    class Meta:
        name = "serviceInstanceQoS"
        namespace = "http://www.ecoa.technology/interface-qos-2.0"
