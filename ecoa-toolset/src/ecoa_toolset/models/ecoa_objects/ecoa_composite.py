# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""ECOA Composite classes.
"""

# Standard library imports
from typing import Dict, List


class ECOAService:
    """"""

    component_name: str = None
    service_name: str = None

    def __init__(self, component_name, service_name):
        self.component_name = component_name
        self.service_name = service_name


class ECOAComponentInstance:
    """"""

    type_name: str = None
    implementation_name: str = None

    def __init__(self, type_name, implementation_name):
        self.type_name = type_name
        self.implementation_name = implementation_name


class ECOAComponentAssembly:
    """"""

    name: str = None
    component_instance: ECOAComponentInstance = None
    properties: Dict[str, str] = None
    services: List[ECOAService] = None

    def __init__(self, name):
        self.name = name
        self.component_instance = None
        self.properties = {}
        self.services = []

    def set_component_instance(self, type_name, implementation_name):
        self.component_instance = ECOAComponentInstance(type_name, implementation_name)

    def add_property(self, name, value):
        self.properties[name] = value

    def add_service(self, name):
        self.services.append(ECOAService(self.name, name))


class ECOAServiceLink:
    """"""

    source: ECOAService = None
    target: ECOAService = None

    def __init__(self, source, target):
        self.source = source
        self.target = target
