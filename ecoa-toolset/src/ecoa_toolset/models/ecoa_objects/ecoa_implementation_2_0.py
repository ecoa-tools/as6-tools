# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/implementation-2.0"


@dataclass
class Instance:
    """
    :ivar name:
    :ivar module_behaviour:
    :ivar relative_priority: Relative priority of this module instance to
              others module instances of the same component instance
              to help
              to distinguish them when allocating actual
              priorities at
              deployment level
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    module_behaviour: Optional[str] = field(default=None, metadata=dict(name="moduleBehaviour", type="Attribute"))
    relative_priority: Optional[int] = field(
        default=None,
        metadata=dict(
            name="relativePriority",
            type="Attribute",
            required=True,
            min_inclusive=0.0,
            max_inclusive=255.0,
        ),
    )


@dataclass
class Use:
    """To define a new Use for a provided or required Component Implementation.

    :ivar library:
    """

    library: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class ModuleImplementation:
    """
    :ivar name:
    :ivar language: Programming language
    :ivar module_type:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    language: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    module_type: Optional[str] = field(default=None, metadata=dict(name="moduleType", type="Attribute", required=True))


@dataclass
class OpRef:
    """
    :ivar instance_name: Reference to a module instance, a service, or
              a reference
    :ivar operation_name:
    """

    instance_name: Optional[str] = field(
        default=None,
        metadata=dict(name="instanceName", type="Attribute", required=True),
    )
    operation_name: Optional[str] = field(
        default=None,
        metadata=dict(name="operationName", type="Attribute", required=True),
    )


@dataclass
class OpRefExternal:
    """Reference used for asynchronous notification coming the legacy code (driver
    component)

    :ivar operation_name:
    :ivar language: Programming language in which the external
              API will be generated for the non-ECOA SW part of the driver
              component
    """

    class Meta:
        name = "OpRef_External"

    operation_name: Optional[str] = field(
        default=None,
        metadata=dict(name="operationName", type="Attribute", required=True),
    )
    language: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class OpRefTrigger:
    """
    :ivar instance_name:
    :ivar period: period in seconds
    """

    class Meta:
        name = "OpRef_Trigger"

    instance_name: Optional[str] = field(
        default=None,
        metadata=dict(name="instanceName", type="Attribute", required=True),
    )
    period: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class Parameter:
    """A parameter a an operation (Event, RequestResponse or VersionedData)

    :ivar name:
    :ivar type:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class PinfoValue:
    """
    :ivar value:
    :ivar name:
    """

    value: Optional[str] = field(
        default=None,
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class PrivatePinfo:
    """Logical name of a private pinfo used by a module.

    :ivar name:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class PropertyValue:
    """
    :ivar value:
    :ivar name:
    """

    value: Optional[str] = field(
        default=None,
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class PublicPinfo:
    """Logical name of a public pinfo used by a module.

    :ivar name:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class ServiceQoS:
    """To define a new QoS for a provided or required service.

    :ivar name:
    :ivar new_qo_s:
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    new_qo_s: Optional[str] = field(default=None, metadata=dict(name="newQoS", type="Attribute", required=True))


@dataclass
class VersionedData:
    """
    :ivar name:
    :ivar type: Type stored by the versioned data.
    :ivar max_versions: Max number of versions accessed at the same
              time.
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    max_versions: int = field(default=1, metadata=dict(name="maxVersions", type="Attribute"))


@dataclass
class DynamicTriggerInstance(Instance):
    """
    :ivar parameter:
    :ivar size: Max number of events waiting for delay
                  expiration in the trigger
    """

    parameter: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    size: int = field(default=1, metadata=dict(type="Attribute"))


@dataclass
class Event:
    """
    :ivar input:
    :ivar name:
    """

    input: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class OpRefActivatable(OpRef):
    """
    :ivar activating: Does the reception of the event/data/rr
                  cause the activation of the receiver module ?
    """

    activating: bool = field(default=True, metadata=dict(type="Attribute"))


@dataclass
class OpRefActivatingFifo(OpRef):
    """
    :ivar fifo_size: Max number of incoming operations that
                  can be stored in the receiver module's FIFO queue for that
                  particular operation link, before the activation
                  of the
                  corresponding entrypoint.
                  There is one fifoSize per
                  operation link on the receiver
                  side.
                  If this max number is
                  exceeded, new incoming operations
                  are discarded.
                  These
                  operations are activating.
    """

    fifo_size: int = field(default=8, metadata=dict(name="fifoSize", type="Attribute"))


@dataclass
class PropertyValues:
    """set of module property values.

    :ivar property_value:
    """

    property_value: List[PropertyValue] = field(
        default_factory=list,
        metadata=dict(
            name="propertyValue",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class RequestResponse:
    """
    :ivar input:
    :ivar output:
    :ivar name:
    """

    input: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    output: List[Parameter] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class TriggerInstance(Instance):
    pass


@dataclass
class ModuleInstance(Instance):
    """Describes an instance of a Module (having its own internal state).

    :ivar property_values:
    :ivar pinfo: Set of pinfo used by the module
    :ivar implementation_name:
    """

    property_values: Optional[PropertyValues] = field(
        default=None,
        metadata=dict(
            name="propertyValues",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
        ),
    )
    pinfo: Optional["ModuleInstance.Pinfo"] = field(
        default=None,
        metadata=dict(type="Element", namespace="http://www.ecoa.technology/implementation-2.0"),
    )
    implementation_name: Optional[str] = field(
        default=None,
        metadata=dict(name="implementationName", type="Attribute", required=True),
    )

    @dataclass
    class Pinfo:
        """
        :ivar public_pinfo:
        :ivar private_pinfo:
        """

        public_pinfo: List[PinfoValue] = field(
            default_factory=list,
            metadata=dict(
                name="publicPinfo",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        private_pinfo: List[PinfoValue] = field(
            default_factory=list,
            metadata=dict(
                name="privatePinfo",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )


@dataclass
class ModuleType:
    """Describes a single-threaded ECOA module, implemented as software,
    contributing to the implementation of an ECOA component.

    :ivar properties: Set of module properties. The value of each
                module property is set at design time.
    :ivar pinfo: Set of pinfo used by the module
    :ivar operations:
    :ivar name:
    :ivar has_user_context: To indicate if the module relies on a user
              context
    :ivar has_warm_start_context: To indicate if the module relies on a warm
              start context
    :ivar is_fault_handler: To indicate if the module is a Fault
              Handler
              or not and to generate fault handling API.
              To enable the
              generation, the platform has to support
              this kind of Fault
              Handler deployment. See Platform
              Procurement Requirements.
    :ivar activating_fault_notifs: Does the reception of fault notifications
              cause the activation of the receiver Fault Handler (only if
              the Fault Handler is implemented as an ECOA component) ?
    """

    properties: Optional["ModuleType.Properties"] = field(
        default=None,
        metadata=dict(type="Element", namespace="http://www.ecoa.technology/implementation-2.0"),
    )
    pinfo: Optional["ModuleType.Pinfo"] = field(
        default=None,
        metadata=dict(type="Element", namespace="http://www.ecoa.technology/implementation-2.0"),
    )
    operations: Optional["ModuleType.Operations"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            required=True,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    has_user_context: bool = field(default=True, metadata=dict(name="hasUserContext", type="Attribute"))
    has_warm_start_context: bool = field(default=True, metadata=dict(name="hasWarmStartContext", type="Attribute"))
    is_fault_handler: bool = field(default=False, metadata=dict(name="isFaultHandler", type="Attribute"))
    activating_fault_notifs: bool = field(default=True, metadata=dict(name="activatingFaultNotifs", type="Attribute"))

    @dataclass
    class Properties:
        """
        :ivar property: The value of each module property is
                          set at design time at instance definition level.
        """

        property: List[Parameter] = field(
            default_factory=list,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=1,
                max_occurs=9223372036854775807,
            ),
        )

    @dataclass
    class Pinfo:
        """
        :ivar public_pinfo:
        :ivar private_pinfo:
        """

        public_pinfo: List[PublicPinfo] = field(
            default_factory=list,
            metadata=dict(
                name="publicPinfo",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        private_pinfo: List[PrivatePinfo] = field(
            default_factory=list,
            metadata=dict(
                name="privatePinfo",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )

    @dataclass
    class Operations:
        """
        :ivar data_written: Read+Write access to a versioned
                          data if writeonly=false. Write only access to a
                          versioned data if writeonly=true.
                          Note: the writeonly attribute is ignored by the
                          Infrastructure if controlled=false on the dataLink.
        :ivar data_read: Read-only access to a versioned data.
        :ivar event_sent:
        :ivar event_received:
        :ivar request_sent:
        :ivar request_received:
        """

        data_written: List["ModuleType.Operations.DataWritten"] = field(
            default_factory=list,
            metadata=dict(
                name="dataWritten",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        data_read: List["ModuleType.Operations.DataRead"] = field(
            default_factory=list,
            metadata=dict(
                name="dataRead",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        event_sent: List[Event] = field(
            default_factory=list,
            metadata=dict(
                name="eventSent",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        event_received: List["ModuleType.Operations.EventReceived"] = field(
            default_factory=list,
            metadata=dict(
                name="eventReceived",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        request_sent: List["ModuleType.Operations.RequestSent"] = field(
            default_factory=list,
            metadata=dict(
                name="requestSent",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        request_received: List["ModuleType.Operations.RequestReceived"] = field(
            default_factory=list,
            metadata=dict(
                name="requestReceived",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )

        @dataclass
        class DataWritten(VersionedData):
            """
            :ivar write_only:
            """

            write_only: bool = field(default=False, metadata=dict(name="writeOnly", type="Attribute"))

        @dataclass
        class DataRead(VersionedData):
            """
            :ivar notifying:
            """

            notifying: bool = field(default=False, metadata=dict(type="Attribute"))

        @dataclass
        class EventReceived(Event):
            pass

        @dataclass
        class RequestSent(RequestResponse):
            """
            :ivar timeout: Timeout value to
                                      unblock/inform respectively a
                                      synchronous/asynchronous RR
                                      If the value is
                                      negative, the timeout
                                      is infinite.
            :ivar is_synchronous:
            :ivar max_concurrent_requests: Max number of concurrent
                                      requests that the module may handle for the
                                      related container call.
            """

            timeout: Optional[Decimal] = field(default=None, metadata=dict(type="Attribute", required=True))
            is_synchronous: Optional[bool] = field(
                default=None,
                metadata=dict(name="isSynchronous", type="Attribute", required=True),
            )
            max_concurrent_requests: int = field(
                default=10,
                metadata=dict(name="maxConcurrentRequests", type="Attribute"),
            )

        @dataclass
        class RequestReceived(RequestResponse):
            """
            :ivar max_concurrent_requests: Max number of concurrent
                                      responses that the module may handle for the
                                      related entry-point, regardless of incoming
                                      requestLinks related to that entry-point.
            """

            max_concurrent_requests: int = field(
                default=10,
                metadata=dict(name="maxConcurrentRequests", type="Attribute"),
            )


@dataclass
class OpRefActivatableFifo(OpRefActivatable):
    """
    :ivar fifo_size: Max number of incoming operations that
                  can be
                  stored in the receiver module's FIFO queue for that
                  particular operation link, before the activation
                  of the
                  corresponding entrypoint.
                  There is one fifoSize per
                  operation link on the receiver side.
                  If this max number is
                  exceeded, new incoming operations are trashed.
    """

    fifo_size: int = field(default=8, metadata=dict(name="fifoSize", type="Attribute"))


@dataclass
class DataLink:
    """Link between DATA operations.

    :ivar writers:
    :ivar readers:
    :ivar id:
    :ivar controlled: Boolean flag to indicate if the Versioned
              Data access are controlled by the Infrastructure.
              If true, each concurrent write accesses to its own copy
              of the data and readers are ensured that the copy they
              access is stable until the release of the VD handle.
              Otherwise, if false, any module getting a handle may
              directly access the local data repository (as no copy is
              made by the Infrastructure).
    """

    writers: Optional["DataLink.Writers"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            required=True,
        ),
    )
    readers: Optional["DataLink.Readers"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
        ),
    )
    id: Optional[int] = field(default=None, metadata=dict(type="Attribute"))
    controlled: bool = field(default=True, metadata=dict(type="Attribute"))

    @dataclass
    class Writers:
        """
        :ivar reference:
        :ivar module_instance:
        """

        reference: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        module_instance: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )

    @dataclass
    class Readers:
        """
        :ivar service:
        :ivar module_instance:
        """

        service: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        module_instance: Optional[List[OpRefActivatableFifo]] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )


@dataclass
class EventLink:
    """Link between EVENT operations.

    :ivar senders:
    :ivar receivers:
    :ivar id:
    """

    senders: Optional["EventLink.Senders"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
        ),
    )
    receivers: Optional["EventLink.Receivers"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            required=True,
        ),
    )
    id: Optional[int] = field(default=None, metadata=dict(type="Attribute"))

    @dataclass
    class Senders:
        """
        :ivar service:
        :ivar reference:
        :ivar module_instance:
        :ivar trigger:
        :ivar dynamic_trigger:
        :ivar external:
        """

        service: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        reference: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        module_instance: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        trigger: Optional[List[OpRefTrigger]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        dynamic_trigger: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                name="dynamicTrigger",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        external: Optional[List[OpRefExternal]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )

    @dataclass
    class Receivers:
        """
        :ivar service:
        :ivar reference:
        :ivar module_instance:
        :ivar dynamic_trigger:
        """

        service: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        reference: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        module_instance: Optional[List[OpRefActivatableFifo]] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        dynamic_trigger: Optional[List[OpRefActivatingFifo]] = field(
            default=None,
            metadata=dict(
                name="dynamicTrigger",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )


@dataclass
class RequestLink:
    """Link between RR operations. Must have exactly one server. Can have many
    clients.

    :ivar clients:
    :ivar server:
    :ivar id:
    """

    clients: Optional["RequestLink.Clients"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            required=True,
        ),
    )
    server: Optional["RequestLink.Server"] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            required=True,
        ),
    )
    id: Optional[int] = field(default=None, metadata=dict(type="Attribute"))

    @dataclass
    class Clients:
        """
        :ivar service:
        :ivar module_instance: Note: attribute 'activating'
                            concerns the response, and is applicable to
                            asynchronous RR operations only.
        """

        service: Optional[List[OpRef]] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )
        module_instance: Optional[List[OpRefActivatable]] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
                min_occurs=0,
                max_occurs=9223372036854775807,
            ),
        )

    @dataclass
    class Server:
        """
        :ivar reference:
        :ivar module_instance: Note: optional attributes concern the
                          request
        """

        reference: Optional[OpRef] = field(
            default=None,
            metadata=dict(
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
            ),
        )
        module_instance: Optional[OpRefActivatableFifo] = field(
            default=None,
            metadata=dict(
                name="moduleInstance",
                type="Element",
                namespace="http://www.ecoa.technology/implementation-2.0",
            ),
        )


@dataclass
class ComponentImplementation:
    """Describes all the information needed to integrate the software
    implementation of an ECOA component in an ECOA system.

    :ivar use:
    :ivar service:
    :ivar reference:
    :ivar module_type:
    :ivar module_implementation:
    :ivar module_instance:
    :ivar trigger_instance:
    :ivar dynamic_trigger_instance:
    :ivar data_link:
    :ivar event_link:
    :ivar request_link:
    :ivar component_definition:
    """

    use: List[Use] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    service: List[ServiceQoS] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    reference: List[ServiceQoS] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    module_type: List[ModuleType] = field(
        default_factory=list,
        metadata=dict(
            name="moduleType",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    module_implementation: List[ModuleImplementation] = field(
        default_factory=list,
        metadata=dict(
            name="moduleImplementation",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    module_instance: List[ModuleInstance] = field(
        default_factory=list,
        metadata=dict(
            name="moduleInstance",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    trigger_instance: List[TriggerInstance] = field(
        default_factory=list,
        metadata=dict(
            name="triggerInstance",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    dynamic_trigger_instance: List[DynamicTriggerInstance] = field(
        default_factory=list,
        metadata=dict(
            name="dynamicTriggerInstance",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    data_link: List[DataLink] = field(
        default_factory=list,
        metadata=dict(
            name="dataLink",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    event_link: List[EventLink] = field(
        default_factory=list,
        metadata=dict(
            name="eventLink",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    request_link: List[RequestLink] = field(
        default_factory=list,
        metadata=dict(
            name="requestLink",
            type="Element",
            namespace="http://www.ecoa.technology/implementation-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    component_definition: Optional[str] = field(
        default=None,
        metadata=dict(name="componentDefinition", type="Attribute", required=True),
    )


@dataclass
class ComponentImplementation(ComponentImplementation):
    class Meta:
        name = "componentImplementation"
        namespace = "http://www.ecoa.technology/implementation-2.0"
