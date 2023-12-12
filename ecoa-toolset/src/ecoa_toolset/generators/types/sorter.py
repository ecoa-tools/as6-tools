# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""TypesSorter class."""

# Standard library imports
from typing import Any, List

# Internal library imports
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class TypesSorter:
    """The Types Sorter.

    Args:
        _ecoa_model : The ECOA Model.
        _library_name (str) : The library name.
        _types (ecoa_types_2_0.DataTypes) : The types.
        _ordered_types (List) : The ordered types.
    """

    def __init__(self, ecoa_model, library_name: str, types: ecoa_types_2_0.DataTypes):
        self._ecoa_model = ecoa_model
        self._library_name = library_name
        self._types = self._construct_types(types)
        self._ordered_types = []

    def _construct_types(self, types: ecoa_types_2_0.DataTypes) -> List:
        types_name = [
            "constant",
            "simple",
            "enum",
            "array",
            "fixed_array",
            "record",
            "variant_record",
        ]
        types_list = []
        for name in types_name:
            tmp = getattr(types, name)
            types_list = [*types_list, *tmp]
        return types_list

    def _find_constant_reference(self, value: str) -> None:
        if value and value[0] == "%" and value[-1] == "%":
            self._find_type_dependency(value[1:-1])

    def _find_type_dependency(self, type_to_find: str) -> None:
        complete_type_to_find = self._ecoa_model.types_helper.add_namespace(type_to_find)
        namespace = self._ecoa_model.types_helper.get_namespace(complete_type_to_find)
        type_name = self._ecoa_model.types_helper.get_name(complete_type_to_find)
        if namespace == self._library_name:
            for other in self._types:
                if other.name == type_name and other not in self._ordered_types:
                    self._find_dependencies(other)

    def _find_dependencies(self, element: Any) -> None:
        if isinstance(element, ecoa_types_2_0.Constant):
            self._find_type_dependency(element.type)
            self._find_constant_reference(element.value)
        elif isinstance(element, ecoa_types_2_0.Enum):
            self._find_type_dependency(element.type)
            for value in element.value:
                self._find_constant_reference(value.valnum)
        elif isinstance(element, ecoa_types_2_0.Simple):
            self._find_type_dependency(element.type)
            self._find_constant_reference(element.min_range)
            self._find_constant_reference(element.max_range)
            self._find_constant_reference(element.precision)
        elif isinstance(element, (ecoa_types_2_0.Array, ecoa_types_2_0.FixedArray)):
            self._find_type_dependency(element.item_type)
            self._find_constant_reference(element.max_number)
        elif isinstance(element, ecoa_types_2_0.Record):
            for field in element.field:
                self._find_type_dependency(field.type)
        elif isinstance(element, ecoa_types_2_0.VariantRecord):
            field_list = {f.type for f in element.field}
            union_list = {f.type for f in element.union}
            all_types = {element.select_type}.union(field_list, union_list)
            for type in all_types:
                self._find_type_dependency(type)
        self._ordered_types.append(element)

    def sort(self) -> List:
        """Sort the types by dependencies.

        Return:
            List : The ordered types.
        """
        if self._ordered_types:
            return self._ordered_types
        for element in self._types:
            if element not in self._ordered_types:
                self._find_dependencies(element)
        return self._ordered_types
