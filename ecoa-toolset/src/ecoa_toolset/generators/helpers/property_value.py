# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""PropertyValueHelper class.
"""

# Internal library imports
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class PropertyValueHelper:
    """Helper to manipulates property values.

    Args:
        _language (str) : The implementation language.
        _types_helper : The types helper.
    """

    _language: str = None
    _types_helper = None

    def __init__(self, language):
        self._language = language

    def _convert_array_items(self, value: str, type_category) -> str:
        item_type_category = self._types_helper.get_type_category(
            self._types_helper.add_namespace(type_category.item_type)
        )
        items = value[1:-1].split(",")
        new_value = value[0]
        if isinstance(type_category, ecoa_types_2_0.Simple) or item_type_category == ecoa_types_2_0.Simple:
            new_value += ",".join([self._convert_simple(item_value.strip()) for item_value in items])
        elif isinstance(item_type_category, ecoa_types_2_0.Enum):
            new_value += ",".join([self._convert_enum(item_value.strip(), item_type_category) for item_value in items])
        new_value += value[-1]
        return new_value

    def _convert_array(self, value: str, type_category, fixed: bool = False) -> str:
        new_value = value
        current_size = 0
        if new_value[0] == "[" and new_value[-1] == "]":
            new_value = self._convert_array_items(new_value.replace("[", "{").replace("]", "}"), type_category)
            current_size = new_value.count(",") + 1
        elif new_value[0] == '"' and new_value[-1] == '"':
            current_size = len(new_value[1:-1]) - new_value[1:-1].count('"') + 1
        if not fixed:
            new_value = "{" + (str(current_size) + ", " if not fixed else "") + new_value + "}"
        return new_value

    def _convert_enum(self, value: str, type_category) -> str:
        type = self._types_helper.add_namespace(type_category.name)
        new_value = value
        if self._language.lower() == "c++":
            new_value = type.replace(":", "::") + "::" + new_value
        elif self._language.lower() == "c":
            new_value = type.replace(":", "__") + "_" + new_value
        return new_value

    def _convert_simple(self, value: str) -> str:
        new_value = value
        if new_value[0] == "%" and new_value[-1] == "%":
            new_value = new_value[1:-1]
            if self._language.lower() == "c++":
                new_value = new_value.replace(":", "::").replace(".", "::")
            elif self._language.lower() == "c":
                new_value = new_value.replace(":", "__").replace(".", "__")
        return new_value

    def convert(self, value: str, type_category, types_helper) -> str:
        """Converts the value of a property to the desired language.

        Args:
            value (str) : The property value.
            type_category : The type category of the property.
            types_helper : The types helper.

        Return:
            new_value (str) : The converted property value.
        """
        self._types_helper = types_helper
        new_value = value
        if isinstance(type_category, ecoa_types_2_0.Array):
            new_value = self._convert_array(new_value, type_category)
        elif isinstance(type_category, ecoa_types_2_0.FixedArray):
            new_value = self._convert_array(new_value, type_category, fixed=True)
        elif isinstance(type_category, ecoa_types_2_0.Enum):
            new_value = self._convert_enum(new_value, type_category)
        elif isinstance(type_category, ecoa_types_2_0.Simple) or type_category == ecoa_types_2_0.Simple:
            new_value = self._convert_simple(new_value)
        return new_value
