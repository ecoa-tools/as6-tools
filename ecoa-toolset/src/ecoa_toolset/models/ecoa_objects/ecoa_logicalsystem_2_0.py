# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/logicalsystem-2.0"


@dataclass
class LogicalComputingNodeLinks:
    """
    :ivar link:
    """

    link: List["LogicalComputingNodeLinks.Link"] = field(
        default_factory=list,
        metadata=dict(type="Element", namespace="", min_occurs=1, max_occurs=9223372036854775807),
    )

    @dataclass
    class Link:
        """
        :ivar throughput:
        :ivar latency:
        :ivar id:
        :ivar to:
        :ivar from_value:
        """

        throughput: Optional["LogicalComputingNodeLinks.Link.Throughput"] = field(
            default=None, metadata=dict(type="Element", namespace="")
        )
        latency: Optional["LogicalComputingNodeLinks.Link.Latency"] = field(
            default=None, metadata=dict(type="Element", namespace="")
        )
        id: Optional[str] = field(default=None, metadata=dict(type="Attribute"))
        to: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
        from_value: Optional[str] = field(default=None, metadata=dict(name="from", type="Attribute", required=True))

        @dataclass
        class Throughput:
            """
            :ivar mega_bytes_per_second:
            """

            mega_bytes_per_second: Optional[int] = field(
                default=None,
                metadata=dict(name="megaBytesPerSecond", type="Attribute", required=True),
            )

        @dataclass
        class Latency:
            """
            :ivar micro_seconds:
            """

            micro_seconds: Optional[int] = field(
                default=None,
                metadata=dict(name="microSeconds", type="Attribute", required=True),
            )


@dataclass
class LogicalComputingPlatformLinks:
    """
    :ivar link:
    """

    link: List["LogicalComputingPlatformLinks.Link"] = field(
        default_factory=list,
        metadata=dict(type="Element", namespace="", min_occurs=1, max_occurs=9223372036854775807),
    )

    @dataclass
    class Link:
        """
        :ivar throughput:
        :ivar latency:
        :ivar transport_binding: Describe on which transport protocol the logical link is associated
                          to
        :ivar id:
        :ivar to:
        :ivar from_value:
        """

        throughput: Optional["LogicalComputingPlatformLinks.Link.Throughput"] = field(
            default=None, metadata=dict(type="Element", namespace="")
        )
        latency: Optional["LogicalComputingPlatformLinks.Link.Latency"] = field(
            default=None, metadata=dict(type="Element", namespace="")
        )
        transport_binding: Optional["LogicalComputingPlatformLinks.Link.TransportBinding"] = field(
            default=None,
            metadata=dict(name="transportBinding", type="Element", namespace=""),
        )
        id: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
        to: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
        from_value: Optional[str] = field(default=None, metadata=dict(name="from", type="Attribute", required=True))

        @dataclass
        class Throughput:
            """
            :ivar mega_bytes_per_second:
            """

            mega_bytes_per_second: Optional[int] = field(
                default=None,
                metadata=dict(name="megaBytesPerSecond", type="Attribute", required=True),
            )

        @dataclass
        class Latency:
            """
            :ivar micro_seconds:
            """

            micro_seconds: Optional[int] = field(
                default=None,
                metadata=dict(name="microSeconds", type="Attribute", required=True),
            )

        @dataclass
        class TransportBinding:
            """
            :ivar protocol:
            :ivar parameters:
            """

            protocol: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
            parameters: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class LogicalComputingPlatform:
    """
    :ivar logical_computing_node:
    :ivar logical_computing_node_links:
    :ivar id:
    :ivar eliplatform_id: Define the Id to be used as Logical ELI Platform ID
              in the ELI generic header
    """

    logical_computing_node: List["LogicalComputingPlatform.LogicalComputingNode"] = field(
        default_factory=list,
        metadata=dict(
            name="logicalComputingNode",
            type="Element",
            namespace="",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    logical_computing_node_links: List[LogicalComputingNodeLinks] = field(
        default_factory=list,
        metadata=dict(
            name="logicalComputingNodeLinks",
            type="Element",
            namespace="",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    id: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    eliplatform_id: Optional[int] = field(default=None, metadata=dict(name="ELIPlatformId", type="Attribute"))

    @dataclass
    class LogicalComputingNode:
        """
        :ivar endianess:
        :ivar logical_processors:
        :ivar os:
        :ivar available_memory:
        :ivar module_switch_time:
        :ivar id:
        """

        endianess: Optional["LogicalComputingPlatform.LogicalComputingNode.Endianess"] = field(
            default=None, metadata=dict(type="Element", namespace="", required=True)
        )
        logical_processors: List["LogicalComputingPlatform.LogicalComputingNode.LogicalProcessors"] = field(
            default_factory=list,
            metadata=dict(
                name="logicalProcessors",
                type="Element",
                namespace="",
                min_occurs=1,
                max_occurs=9223372036854775807,
            ),
        )
        os: Optional["LogicalComputingPlatform.LogicalComputingNode.Os"] = field(
            default=None, metadata=dict(type="Element", namespace="", required=True)
        )
        available_memory: Optional["LogicalComputingPlatform.LogicalComputingNode.AvailableMemory"] = field(
            default=None,
            metadata=dict(name="availableMemory", type="Element", namespace="", required=True),
        )
        module_switch_time: Optional["LogicalComputingPlatform.LogicalComputingNode.ModuleSwitchTime"] = field(
            default=None,
            metadata=dict(name="moduleSwitchTime", type="Element", namespace="", required=True),
        )
        id: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))

        @dataclass
        class Endianess:
            """
            :ivar type:
            """

            type: Optional["LogicalComputingPlatform.LogicalComputingNode.Endianess.Type"] = field(
                default=None, metadata=dict(type="Attribute", required=True)
            )

            class Type(Enum):
                """
                :cvar BIG:
                :cvar LITTLE:
                """

                BIG = "BIG"
                LITTLE = "LITTLE"

        @dataclass
        class LogicalProcessors:
            """
            :ivar step_duration:
            :ivar type:
            :ivar number:
            """

            step_duration: Optional[
                "LogicalComputingPlatform.LogicalComputingNode.LogicalProcessors.StepDuration"
            ] = field(
                default=None,
                metadata=dict(name="stepDuration", type="Element", namespace="", required=True),
            )
            type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
            number: Optional[int] = field(default=None, metadata=dict(type="Attribute", required=True))

            @dataclass
            class StepDuration:
                """
                :ivar nano_seconds:
                """

                nano_seconds: Optional[int] = field(
                    default=None,
                    metadata=dict(name="nanoSeconds", type="Attribute", required=True),
                )

        @dataclass
        class Os:
            """
            :ivar name:
            :ivar version:
            """

            name: Optional["LogicalComputingPlatform.LogicalComputingNode.Os.Name"] = field(
                default=None, metadata=dict(type="Attribute", required=True)
            )
            version: Optional[str] = field(default=None, metadata=dict(type="Attribute"))

            class Name(Enum):
                """
                :cvar FASTOS:
                :cvar LINUX:
                :cvar IMA_INTEGRITY:
                :cvar IMS_VXWORKS:
                :cvar INTEGRITY:
                :cvar PIKEOS:
                :cvar RTEMS:
                :cvar VXWORKS:
                :cvar VXWORKS_ARINC653:
                :cvar VXWORKS_CERT:
                :cvar WINDOWS:
                :cvar ZEPHYR:
                """

                FASTOS = "fastos"
                LINUX = "linux"
                IMA_INTEGRITY = "ima-integrity"
                IMS_VXWORKS = "ims-vxworks"
                INTEGRITY = "integrity"
                PIKEOS = "pikeos"
                RTEMS = "rtems"
                VXWORKS = "vxworks"
                VXWORKS_ARINC653 = "vxworks-arinc653"
                VXWORKS_CERT = "vxworks-cert"
                WINDOWS = "windows"
                ZEPHYR = "zephyr"

        @dataclass
        class AvailableMemory:
            """
            :ivar giga_bytes:
            """

            giga_bytes: Optional[int] = field(
                default=None,
                metadata=dict(name="gigaBytes", type="Attribute", required=True),
            )

        @dataclass
        class ModuleSwitchTime:
            """
            :ivar micro_seconds:
            """

            micro_seconds: Optional[int] = field(
                default=None,
                metadata=dict(name="microSeconds", type="Attribute", required=True),
            )


@dataclass
class LogicalSystem:
    """
    :ivar logical_computing_platform:
    :ivar logical_computing_platform_links:
    :ivar id:
    """

    logical_computing_platform: List[LogicalComputingPlatform] = field(
        default_factory=list,
        metadata=dict(
            name="logicalComputingPlatform",
            type="Element",
            namespace="",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    logical_computing_platform_links: List[LogicalComputingPlatformLinks] = field(
        default_factory=list,
        metadata=dict(
            name="logicalComputingPlatformLinks",
            type="Element",
            namespace="",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    id: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class LogicalSystem(LogicalSystem):
    class Meta:
        name = "logicalSystem"
        namespace = "http://www.ecoa.technology/logicalsystem-2.0"
