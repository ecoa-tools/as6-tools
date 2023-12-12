# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.ecoa.technology/cross-platforms-view-2.0"


@dataclass
class Composite:
    """
    :ivar name:
    :ivar deployed_on_computing_platform: Name of a logical platform
    """

    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    deployed_on_computing_platform: Optional[str] = field(
        default=None,
        metadata=dict(name="deployedOnComputingPlatform", type="Attribute", required=True),
    )


@dataclass
class EuidsBinding:
    """
    :ivar specific_binding: specific EUIDS file associated to one given
                peer of the link
    :ivar euids: Bind an EUIDS file to a given logical
              computing platform link
    :ivar bound_to_link_id: Reference an inter-platform link
              identified in
              the logical system
    """

    class Meta:
        name = "EUIDsBinding"

    specific_binding: List["EuidsBinding.SpecificBinding"] = field(
        default_factory=list,
        metadata=dict(
            name="specificBinding",
            type="Element",
            namespace="http://www.ecoa.technology/cross-platforms-view-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    euids: Optional[str] = field(default=None, metadata=dict(name="EUIDs", type="Attribute", required=True))
    bound_to_link_id: Optional[str] = field(
        default=None,
        metadata=dict(name="boundToLinkId", type="Attribute", required=True),
    )

    @dataclass
    class SpecificBinding:
        """
        :ivar euids: specific EUIDS file associated to one
                        given peer of the link
        :ivar bound_to_computing_platform: Name of a logical platform
        """

        euids: Optional[str] = field(default=None, metadata=dict(name="EUIDs", type="Attribute", required=True))
        bound_to_computing_platform: Optional[str] = field(
            default=None,
            metadata=dict(name="boundToComputingPlatform", type="Attribute", required=True),
        )


@dataclass
class WireMapping:
    """
    :ivar source: wire source
    :ivar target: wire target
    :ivar mapped_on_link_id: reference an inter-platform link
              identified in
              the logical system
    """

    source: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    target: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    mapped_on_link_id: Optional[str] = field(
        default=None,
        metadata=dict(name="mappedOnLinkId", type="Attribute", required=True),
    )


@dataclass
class View:
    """Describes how composites are mapped onto platforms, how wires are mapped
    onto logical links and how IDs are bound to logical links.

    :ivar composite: Defines where a composite is executed
    :ivar wire_mapping: Defines the mapping of a wires onto a
                  logical
                  platform link
    :ivar euids_binding: Defines the binding of EUIDs onto a
                  logical platform link
    :ivar name:
    :ivar assembly: Name of the system composite referenced by
              this view
    :ivar logical_system: Name of the logical system this deployment is
              made on
    """

    composite: List[Composite] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/cross-platforms-view-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    wire_mapping: List[WireMapping] = field(
        default_factory=list,
        metadata=dict(
            name="wireMapping",
            type="Element",
            namespace="http://www.ecoa.technology/cross-platforms-view-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    euids_binding: List[EuidsBinding] = field(
        default_factory=list,
        metadata=dict(
            name="euidsBinding",
            type="Element",
            namespace="http://www.ecoa.technology/cross-platforms-view-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    assembly: Optional[str] = field(default=None, metadata=dict(type="Attribute", required=True))
    logical_system: Optional[str] = field(
        default=None,
        metadata=dict(name="logicalSystem", type="Attribute", required=True),
    )


@dataclass
class View(View):
    class Meta:
        name = "view"
        namespace = "http://www.ecoa.technology/cross-platforms-view-2.0"
