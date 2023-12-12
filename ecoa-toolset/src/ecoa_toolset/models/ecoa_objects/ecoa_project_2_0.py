# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/project-2.0"


@dataclass
class EliEuids:
    """List of bindings.

    :ivar euid:
    """

    class Meta:
        name = "ELI_EUIDs"

    euid: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="EUID",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class Files:
    """List of files.

    :ivar file:
    """

    file: List[str] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class EcoaProject:
    """Describes a whole ECOA project.

    :ivar service_definitions:
    :ivar component_definitions:
    :ivar types:
    :ivar initial_assembly:
    :ivar component_implementations:
    :ivar logical_system:
    :ivar cross_platforms_view:
    :ivar deployment_schema:
    :ivar output_directory:
    :ivar implementation_assembly:
    :ivar euids:
    :ivar name:
    """

    service_definitions: List[Files] = field(
        default_factory=list,
        metadata=dict(
            name="serviceDefinitions",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    component_definitions: List[Files] = field(
        default_factory=list,
        metadata=dict(
            name="componentDefinitions",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    types: List[Files] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    initial_assembly: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="initialAssembly",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    component_implementations: List[Files] = field(
        default_factory=list,
        metadata=dict(
            name="componentImplementations",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    logical_system: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="logicalSystem",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    cross_platforms_view: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="crossPlatformsView",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    deployment_schema: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="deploymentSchema",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    output_directory: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="outputDirectory",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    implementation_assembly: List[str] = field(
        default_factory=list,
        metadata=dict(
            name="implementationAssembly",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    euids: List[EliEuids] = field(
        default_factory=list,
        metadata=dict(
            name="EUIDs",
            type="Element",
            namespace="http://www.ecoa.technology/project-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))


@dataclass
class Ecoaproject(EcoaProject):
    class Meta:
        name = "ECOAProject"
        namespace = "http://www.ecoa.technology/project-2.0"
