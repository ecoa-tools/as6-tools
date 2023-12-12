# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""PropertiesChecker class.
"""

# Standard library imports
import re

# Internal library imports
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class PropertiesChecker:
    """Checker of properties at type and value levels.

    Args:
        _ecoa_model : The ECOA model.
    """

    _ecoa_model = None

    def __init__(self, ecoa_model):
        self._ecoa_model = ecoa_model

    def _is_simple_type(self, type_category) -> bool:
        return (
            isinstance(type_category, ecoa_types_2_0.Enum)
            or isinstance(type_category, ecoa_types_2_0.Simple)
            or type_category == ecoa_types_2_0.Simple
        )

    def _check_type(
        self, component_impl_name: str, module_type_name: str, name: str, complete_type: str, type_category
    ) -> None:
        unsupported = False
        if isinstance(type_category, ecoa_types_2_0.Array) or isinstance(type_category, ecoa_types_2_0.FixedArray):
            item_type_category = self._ecoa_model.types_helper.get_type_category(
                self._ecoa_model.types_helper.add_namespace(type_category.item_type)
            )
            if not self._is_simple_type(item_type_category):
                unsupported = True
        elif not self._is_simple_type(type_category):
            unsupported = True
        if unsupported:
            raise ValueError(
                f"Unsupported type {complete_type} for property {component_impl_name}:{module_type_name}:{name}"
            )

    def _check_array_length(
        self, component_impl_name: str, module_inst_name: str, name: str, length: str, type_category
    ) -> None:
        if isinstance(type_category, ecoa_types_2_0.Array) and length > int(type_category.max_number):
            raise ValueError(
                f"Incorrect array length ({length}>{int(type_category.max_number)}) for property value "
                + f"{component_impl_name}:{module_inst_name}:{name}"
            )
        elif isinstance(type_category, ecoa_types_2_0.FixedArray) and length != int(type_category.max_number):
            raise ValueError(
                f"Incorrect array length ({length}!={int(type_category.max_number)}) for property value "
                + f"{component_impl_name}:{module_inst_name}:{name}"
            )

    def _check_array_value(
        self, component_impl_name: str, module_inst_name: str, name: str, value: str, type_category
    ) -> None:
        item_type_category = self._ecoa_model.types_helper.get_type_category(
            self._ecoa_model.types_helper.add_namespace(type_category.item_type)
        )
        if value[0] == "[" and value[-1] == "]":
            items = value[1:-1].split(",")
            for item in items:
                self._check_value(
                    component_impl_name, module_inst_name, name, item.replace(" ", ""), item_type_category
                )
            self._check_array_length(component_impl_name, module_inst_name, name, len(items), type_category)
        elif value[0] == '"' and value[-1] == '"':
            self._check_array_length(
                component_impl_name,
                module_inst_name,
                name,
                len(value[1:-1]) - value[1:-1].count('"') + 1,
                type_category,
            )
        else:
            raise ValueError(
                f"Unsupported array value {value} for property value {component_impl_name}:{module_inst_name}:{name}"
            )

    def _check_unknown_symbols(self, component_impl_name: str, module_inst_name: str, name: str, value: str) -> None:
        match = re.search(r"#?(\d|\*):", value)
        if match:
            raise ValueError(
                f"Unknown symbol {match.group(0)} in value {value} for property value "
                + f"{component_impl_name}:{module_inst_name}:{name}"
            )

    def _check_enum_value(
        self, component_impl_name: str, module_inst_name: str, name: str, value: str, type_category
    ) -> None:
        self._check_unknown_symbols(component_impl_name, module_inst_name, name, value)
        values = [enum_value.name for enum_value in type_category.value]
        if value not in values:
            raise ValueError(
                f"Unknown enum value {value} for property value {component_impl_name}:{module_inst_name}:{name}"
            )

    def _check_simple_value(self, component_impl_name: str, module_inst_name: str, name: str, value: str) -> None:
        self._check_unknown_symbols(component_impl_name, module_inst_name, name, value)
        if value[0] == "%" and value[-1] == "%":
            constant_type_category = self._ecoa_model.types_helper.get_type_category(
                self._ecoa_model.types_helper.add_namespace(value[1:-1])
            )
            if not constant_type_category:
                raise ValueError(
                    f"Unknown constant value {value} for property value {component_impl_name}:{module_inst_name}:{name}"
                )

    def _check_value(
        self, component_impl_name: str, module_inst_name: str, name: str, value: str, type_category
    ) -> None:
        if isinstance(type_category, ecoa_types_2_0.Array) or isinstance(type_category, ecoa_types_2_0.FixedArray):
            self._check_array_value(component_impl_name, module_inst_name, name, value, type_category)
        elif isinstance(type_category, ecoa_types_2_0.Enum):
            self._check_enum_value(component_impl_name, module_inst_name, name, value, type_category)
        elif isinstance(type_category, ecoa_types_2_0.Simple) or type_category == ecoa_types_2_0.Simple:
            self._check_simple_value(component_impl_name, module_inst_name, name, value)

    def compute(self) -> None:
        """Checks for each parsed property :
        - if the type is a simple, an enum or an (fixed) array of simple or enums
        - if the value is well written and does not contain unrecognized symbols
        """
        for k, v in self._ecoa_model.properties.items():
            for property in v:
                component_impl_name = k.split(":")[0]
                module_type_name = self._ecoa_model.module_impls.get(k).module_type
                module_inst_name = None
                for module_inst in self._ecoa_model.module_insts.values():
                    if module_inst.implementation_name == property.module_impl_name:
                        module_inst_name = module_inst.name
                        break
                name = property.name
                complete_type = property.namespace + ":" + property.type
                type_category = property.type_category
                self._check_type(component_impl_name, module_type_name, name, complete_type, type_category)
                for value in property.values.values():
                    self._check_value(component_impl_name, module_inst_name, name, value, type_category)
