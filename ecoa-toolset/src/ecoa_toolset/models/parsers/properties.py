# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""PropertiesParser class.
"""

# Standard library imports
from typing import Dict

# Internal library imports
from ecoa_toolset.models.components import Property
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class PropertiesParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name

    def _build_type(self, property):
        type = self._ecoa_model.types_helper.add_namespace(property.type)
        type_category = self._ecoa_model.types_helper.get_type_category(type)
        if isinstance(type_category, ecoa_types_2_0.Constant):
            type = self._ecoa_model.types_helper.add_namespace(type_category.type)
            type_category = self._ecoa_model.types_helper.get_type_category(type)
        return type, type_category

    def _build_values(self, module_impl, property) -> Dict:
        property_values = {}
        for key, module_inst in self._ecoa_model.module_insts.items():
            if (
                self._component_impl_name == ":".join(key.split(":")[:-1])
                and module_inst.implementation_name == module_impl.name
            ):
                for pv in module_inst.property_values.property_value:
                    if pv.name == property.name:
                        property_values[key] = pv.value.strip()
                        break
        tmp = {}
        for key, property_value in property_values.items():
            for component_name in self._ecoa_model.component_names.get(key):
                k = key + ":" + component_name
                if property_value[0] == "$":
                    for ci in self._ecoa_model.ecoa_xml_model._components_assembly.values():
                        if ci.name == component_name:
                            tmp[k] = ci.properties[property_value[1:]]
                else:
                    tmp[k] = property_value
        property_values = tmp
        return property_values

    def _build(self, module_impl, property) -> None:
        type, type_category = self._build_type(property)
        values = self._build_values(module_impl, property)
        property = Property(
            self._component_impl_name,
            module_impl.name,
            module_impl.language.lower(),
            property.name,
            type.split(":")[0],
            type.split(":")[1],
            type_category,
            values,
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.properties:
            self._ecoa_model.properties[key].append(property)
        else:
            self._ecoa_model.properties[key] = [property]

    def _add_all(self, module_impl, properties) -> None:
        for property in properties:
            self._build(module_impl, property)

    def compute(self) -> None:
        for module_impl in self._component_implementation.module_implementation:
            module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
            if module_type.properties and module_type.properties.property:
                self._add_all(module_impl, module_type.properties.property)
