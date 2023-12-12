# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""TypeHelper class.
"""

# Standard library imports
from typing import ClassVar, Dict, List

# Internal library imports
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class TypeHelper:
    """Helper to manipulates ECOA types."""

    ecoa_types: ClassVar[Dict] = {
        "boolean8": ecoa_types_2_0.Simple,
        "int8": ecoa_types_2_0.Simple,
        "char8": ecoa_types_2_0.Simple,
        "byte": ecoa_types_2_0.Simple,
        "int16": ecoa_types_2_0.Simple,
        "int32": ecoa_types_2_0.Simple,
        "uint8": ecoa_types_2_0.Simple,
        "uint16": ecoa_types_2_0.Simple,
        "uint32": ecoa_types_2_0.Simple,
        "float32": ecoa_types_2_0.Simple,
        "double64": ecoa_types_2_0.Simple,
        "int64": ecoa_types_2_0.Simple,
        "uint64": ecoa_types_2_0.Simple,
        "return_status": ecoa_types_2_0.Simple,
        "hr_time": ecoa_types_2_0.Record,
        "global_time": ecoa_types_2_0.Record,
        "duration": ecoa_types_2_0.Record,
        "log": ecoa_types_2_0.Record,
        "error_id": ecoa_types_2_0.Simple,
        "error_code": ecoa_types_2_0.Simple,
        "asset_id": ecoa_types_2_0.Simple,
        "asset_type": ecoa_types_2_0.Simple,
        "error_type": ecoa_types_2_0.Simple,
        "recovery_action_type": ecoa_types_2_0.Simple,
        "pinfo_filename": ecoa_types_2_0.Record,
        "seek_whence_type": ecoa_types_2_0.Simple,
    }

    _ecoa_model = None

    def __init__(self, ecoa_model) -> None:
        self._ecoa_model = ecoa_model

    def find_all(self, namespace: str = None, type_name: str = None, category: List[str] = []) -> Dict:
        """Search in ECOA model library types.

        Args:
            - namespace (str)
            - type_name (str)
            - category (list)
                - Array
                - Constant
                - Enum
                - FixedArray
                - Simple
                - Record
                - VariantRecord
                - Union

        Returns:
            A dictionary of types

        Comments:
            cf. models/ecoa_objects/ecoa_types_2_0.py
        """
        filtered = None
        if namespace and not type_name:
            filtered = {
                k: v for k, v in self._ecoa_model.types.items() if k.startswith(f"{namespace.replace('.', '__')}:")
            }
        elif type_name and not namespace:
            filtered = {k: v for k, v in self._ecoa_model.types.items() if k.endswith(f":{type_name}")}
        elif type_name and namespace:
            filtered = {
                k: v for k, v in self._ecoa_model.types.items() if f"{namespace.replace('.', '__')}:{type_name}" in k
            }
        else:
            filtered = self._ecoa_model.types
        if category:
            filtered = {k: v for k, v in filtered.items() if type(v).__name__ in category}
        return filtered

    def find_one(self, complete_name: str = None, namespace: str = None, type_name: str = None) -> Dict:
        """Search the first type that matches with the query in ECOA model library types.

        Args:
            - complete_name (str)
            - namespace (str)
            - type_name (str)

        Returns:
            A dict that matches with the query

        Comments:
            cf. models/ecoa_objects/ecoa_types_2_0.py
        """
        if complete_name:
            if complete_name.startswith("ECOA:"):
                return {complete_name: self.ecoa_types.get(self.get_name(complete_name), None)}
            else:
                return {complete_name: self._ecoa_model.types.get(complete_name.replace(".", "__"), None)}
        elif type_name:
            try:
                return next(iter(self.find_all(type_name=type_name).items()))
            except StopIteration:
                pass
        elif namespace:
            try:
                return next(iter(self.find_all(namespace=namespace).items()))
            except StopIteration:
                pass
        return None

    def add_namespace(self, type_name: str = None) -> str:
        """Add the correct namespace to the type name if not exists.

        Args:
            - type_name (str)

        Returns:
            A type with its namespace (str)
        """
        if ":" not in type_name:
            match = self.find_one(type_name=type_name)
            if match is not None:
                type_name = next(iter(match))
            elif type_name in self.ecoa_types:
                type_name = self.build_complete_type("ECOA", type_name)
        return type_name

    def build_complete_type(self, namespace: str, type_name: str) -> str:
        """Build a complete type name.

        Args:
            - namespace (str)
            - type_name (str)

        Returns:
            A complete type (str)
        """
        return f"{namespace}:{type_name}"

    def get_namespace(self, complete_type_name: str) -> str:
        """Gets the first element of the complete type name.

        Args:
            - complete_type_name (str)

        Returns:
            The namespace of the complete type (str)
        """
        try:
            result = complete_type_name.split(":")
            if len(result) == 2:
                return complete_type_name.split(":")[0]
            return None
        except IndexError:
            return None

    def get_name(self, complete_type_name: str) -> str:
        """Gets the second element of the complete type name.

        Args:
            - complete_type_name (str)

        Returns:
            The name of the complete type (str)
        """
        try:
            return complete_type_name.split(":")[1]
        except IndexError:
            return None

    def get_type_category(self, complete_type_name: str) -> str:
        """Gets the element type category.

        Args:
            - complete_type_name (str)

        Returns:
            The element type category
        """
        return self.find_one(complete_name=complete_type_name).get(complete_type_name)
