# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/deployment-2.0"


@dataclass
class ComputingNodeConfiguration:
    """
    :ivar computing_node: Id of a logical computing node
    :ivar scheduling_information: Link to any external file containing any
              additional scheduling parameters required by the system
              integrator (non-defined by ECOA)
    """

    computing_node: Optional[str] = field(
        default=None,
        metadata=dict(name="computingNode", type="Attribute", required=True),
    )
    scheduling_information: Optional[str] = field(
        default=None, metadata=dict(name="schedulingInformation", type="Attribute")
    )


@dataclass
class ModuleLog:
    """Defines level of logging for a deployed module instance.

    :ivar instance_name:
    :ivar enabled_levels:
    """

    instance_name: Optional[str] = field(
        default=None,
        metadata=dict(name="instanceName", type="Attribute", required=True),
    )
    enabled_levels: Optional[str] = field(
        default=None,
        metadata=dict(name="enabledLevels", type="Attribute", required=True),
    )


@dataclass
class PlatformMessages:
    """
    :ivar mapped_on_link_id: Refers to the inter-platforms link
              on which the platform-level management messages
              are mapped. The link is defined in
              the logical system.
    """

    mapped_on_link_id: Optional[str] = field(
        default=None,
        metadata=dict(name="mappedOnLinkId", type="Attribute", required=True),
    )


@dataclass
class ProtectionDomain:
    """Defines an OS executable, offering memory (and possibly also temporal)
    protection.

    :ivar execute_on:
    :ivar deployed_module_instance:
    :ivar deployed_trigger_instance:
    :ivar name:
    """

    execute_on: Optional["ProtectionDomain.ExecuteOn"] = field(
        default=None,
        metadata=dict(
            name="executeOn",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            required=True,
        ),
    )
    deployed_module_instance: List["ProtectionDomain.DeployedModuleInstance"] = field(
        default_factory=list,
        metadata=dict(
            name="deployedModuleInstance",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    deployed_trigger_instance: List["ProtectionDomain.DeployedTriggerInstance"] = field(
        default_factory=list,
        metadata=dict(
            name="deployedTriggerInstance",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))

    @dataclass
    class ExecuteOn:
        """
        :ivar computing_node:
        :ivar computing_platform: Id of a logical system.
        """

        computing_node: Optional[str] = field(
            default=None,
            metadata=dict(name="computingNode", type="Attribute", required=True),
        )
        computing_platform: Optional[str] = field(
            default=None,
            metadata=dict(name="computingPlatform", type="Attribute", required=True),
        )

    @dataclass
    class DeployedModuleInstance:
        """
        :ivar component_name:
        :ivar module_instance_name:
        :ivar module_priority: Abstract module priority that can be
                          used by the platform to map the module on an
                          actual OS priority
        """

        component_name: Optional[str] = field(
            default=None,
            metadata=dict(name="componentName", type="Attribute", required=True),
        )
        module_instance_name: Optional[str] = field(
            default=None,
            metadata=dict(name="moduleInstanceName", type="Attribute", required=True),
        )
        module_priority: Optional[Decimal] = field(
            default=None,
            metadata=dict(
                name="modulePriority",
                type="Attribute",
                required=True,
                min_inclusive=0.0,
                max_inclusive=255.0,
            ),
        )

    @dataclass
    class DeployedTriggerInstance:
        """
        :ivar component_name:
        :ivar trigger_instance_name:
        :ivar trigger_priority: Abstract trigger priority that can be
                          used by the platform to map the trigger on an actual
                          OS priority
        """

        component_name: Optional[str] = field(
            default=None,
            metadata=dict(name="componentName", type="Attribute", required=True),
        )
        trigger_instance_name: Optional[str] = field(
            default=None,
            metadata=dict(name="triggerInstanceName", type="Attribute", required=True),
        )
        trigger_priority: Optional[Decimal] = field(
            default=None,
            metadata=dict(
                name="triggerPriority",
                type="Attribute",
                required=True,
                min_inclusive=0.0,
                max_inclusive=255.0,
            ),
        )


@dataclass
class WireMapping:
    """Defines a mapping between a wire and a computing platform link.

    :ivar source: Wire Source
    :ivar target: Wire Target
    :ivar mapped_on_link_id: Refers to the inter-nodes
              or the inter-platforms link
              on which the wire is mapped. The link is
              is defined at platform description level
              in the logical system.
    """

    source: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    target: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    mapped_on_link_id: Optional[str] = field(
        default=None,
        metadata=dict(name="mappedOnLinkId", type="Attribute", required=True),
    )


@dataclass
class ComponentLog:
    """Defines default level of logging for a given component.

    :ivar module_log:
    :ivar instance_name:
    :ivar enabled_levels:
    """

    module_log: List[ModuleLog] = field(
        default_factory=list,
        metadata=dict(
            name="moduleLog",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    instance_name: Optional[str] = field(
        default=None,
        metadata=dict(name="instanceName", type="Attribute", required=True),
    )
    enabled_levels: Optional[str] = field(
        default=None,
        metadata=dict(name="enabledLevels", type="Attribute", required=True),
    )


@dataclass
class PlatformConfiguration:
    """
    :ivar computing_node_configuration: Defines the computing node level
                configuration
    :ivar platform_messages: Define on which the platform
                domain messages are mapped
    :ivar computing_platform: Id of a logical system.
    :ivar fault_handler_notification_max_number: Defines the number of fault handler
              notifications that a Module Container shall be able
              to handle at any time. These notifications are
              relevant depending on the Module “isFaultHandler”
              attribute.
    :ivar euids: Specific EUIDS file associated to one
              given peer of the link
    """

    computing_node_configuration: List[ComputingNodeConfiguration] = field(
        default_factory=list,
        metadata=dict(
            name="computingNodeConfiguration",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    platform_messages: List[PlatformMessages] = field(
        default_factory=list,
        metadata=dict(
            name="platformMessages",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    computing_platform: Optional[str] = field(
        default=None,
        metadata=dict(name="computingPlatform", type="Attribute", required=True),
    )
    fault_handler_notification_max_number: Decimal = field(
        default=Decimal("8"),
        metadata=dict(
            name="faultHandlerNotificationMaxNumber",
            type="Attribute",
            min_inclusive=1.0,
            max_inclusive=255.0,
        ),
    )
    euids: Optional[str] = field(default=None, metadata=dict(name="EUIDs", type="Attribute"))


@dataclass
class LogPolicy:
    """Defines the log policy for deployed components and modules.

    :ivar component_log:
    """

    component_log: List[ComponentLog] = field(
        default_factory=list,
        metadata=dict(
            name="componentLog",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class Deployment:
    """
    :ivar protection_domain:
    :ivar log_policy:
    :ivar platform_configuration: Defines platform-wide settings
    :ivar wire_mapping: Defines a mapping between a wire and a
                computing platform link
    :ivar final_assembly: Name of the composite referenced by this
              deployment
    :ivar logical_system: Name of the logical system this deployment is
              made on
    """

    protection_domain: List[ProtectionDomain] = field(
        default_factory=list,
        metadata=dict(
            name="protectionDomain",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    log_policy: List[LogPolicy] = field(
        default_factory=list,
        metadata=dict(
            name="logPolicy",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    platform_configuration: List[PlatformConfiguration] = field(
        default_factory=list,
        metadata=dict(
            name="platformConfiguration",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    wire_mapping: List[WireMapping] = field(
        default_factory=list,
        metadata=dict(
            name="wireMapping",
            type="Element",
            namespace="http://www.ecoa.technology/deployment-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    final_assembly: Optional[str] = field(
        default=None,
        metadata=dict(name="finalAssembly", type="Attribute", required=True),
    )
    logical_system: Optional[str] = field(
        default=None,
        metadata=dict(name="logicalSystem", type="Attribute", required=True),
    )


@dataclass
class Deployment(Deployment):
    class Meta:
        name = "deployment"
        namespace = "http://www.ecoa.technology/deployment-2.0"
