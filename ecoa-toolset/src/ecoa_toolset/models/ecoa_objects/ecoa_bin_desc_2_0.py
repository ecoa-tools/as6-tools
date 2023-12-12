# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/bin-desc-2.0"


@dataclass
class BinaryDependency:
    """binary dependency that needs to be linked with the initial object.

    :ivar object: Filename of the binary implementing the
              referenced dependency
    :ivar checksum: Checksum of the binary dependency
    """

    object: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    checksum: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute", required=True, pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0"),
    )


@dataclass
class ProcessorTarget:
    """ "Identification of the processor for which modules have been compiled".

    :ivar type:
    """

    type: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class BinaryModule:
    """Technical description of the binary module.

    :ivar binary_dependency:
    :ivar reference: Name of the module implementation
    :ivar object: Filename of the binary implementing the
              referenced module. The filename may contain path information
              relative to the bin-desc location e.g. "binaries/module.o"
              relates a file 'module.o' located in a subdirectory 'binaries'
              of the directory containing the bin-desc file. Separators are
              '/'
    :ivar user_context_size: Size in bytes of the module user context
    :ivar warm_start_context_size: Size in bytes of the module warm start
              context
    :ivar stack_size: maximum size in bytes of the stack used by
              any module entry point (including all sub-function calls)
    :ivar heap_size: maximum size in bytes of the heap (memory
              dynamically allocated by the module binary itself: malloc or
              object instances)
    :ivar checksum: Checksum of the binary
    """

    binary_dependency: List[BinaryDependency] = field(
        default_factory=list,
        metadata=dict(
            name="binaryDependency",
            type="Element",
            namespace="http://www.ecoa.technology/bin-desc-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    reference: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    object: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    user_context_size: Optional[str] = field(
        default=None,
        metadata=dict(
            name="userContextSize",
            type="Attribute",
            required=True,
            pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0",
        ),
    )
    warm_start_context_size: Optional[str] = field(
        default=None,
        metadata=dict(
            name="warmStartContextSize",
            type="Attribute",
            required=True,
            pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0",
        ),
    )
    stack_size: Optional[str] = field(
        default=None,
        metadata=dict(
            name="stackSize",
            type="Attribute",
            required=True,
            pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0",
        ),
    )
    heap_size: Optional[str] = field(
        default=None,
        metadata=dict(
            name="heapSize",
            type="Attribute",
            required=True,
            pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0",
        ),
    )
    checksum: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute", required=True, pattern=r"0x[0-9A-Fa-f]+|[1-9][0-9]*|0"),
    )


@dataclass
class BinDesc:
    """Links between module implementations and binary objects.

    :ivar processor_target:
    :ivar binary_module:
    :ivar component_implementation:
    :ivar insertion_policy: Link to an external table containing
              insertion policy data of the binary ECOA component
    """

    processor_target: Optional[ProcessorTarget] = field(
        default=None,
        metadata=dict(
            name="processorTarget",
            type="Element",
            namespace="http://www.ecoa.technology/bin-desc-2.0",
            required=True,
        ),
    )
    binary_module: List[BinaryModule] = field(
        default_factory=list,
        metadata=dict(
            name="binaryModule",
            type="Element",
            namespace="http://www.ecoa.technology/bin-desc-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    component_implementation: Optional[str] = field(
        default=None,
        metadata=dict(
            name="componentImplementation",
            type="Attribute",
            required=True,
            pattern=r"[A-Za-z][A-Za-z0-9_]*",
        ),
    )
    insertion_policy: Optional[str] = field(default=None, metadata=dict(name="insertionPolicy", type="Attribute"))


@dataclass
class BinDesc(BinDesc):
    class Meta:
        name = "binDesc"
        namespace = "http://www.ecoa.technology/bin-desc-2.0"
