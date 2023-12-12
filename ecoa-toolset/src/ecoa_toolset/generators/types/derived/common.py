# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Common attributes for types generation.
"""

# Standard library imports
from typing import Dict, List

# Internal library imports
from ecoa_toolset.generators.common import Common as GlobalCommon
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0
from ecoa_toolset.models.helpers.type import TypeHelper


class Common(GlobalCommon):
    """"""

    _constant_suffixes: Dict = {
        "int32": "L",
        "uint32": "UL",
        "int64": "LL",
        "uint64": "LLU",
        "float32": "F",
    }

    @classmethod
    def construct_type(cls, variable_type: str, library_name: str, language: str):
        generation = ""
        if ":" in variable_type:
            generation += variable_type
        elif variable_type in TypeHelper.ecoa_types:
            generation += "ECOA:" + variable_type
        else:
            generation += cls.switch_lang(library_name + ":", "", language) + variable_type
        generation = generation.replace(":", cls.switch_lang("__", "::", language))
        generation = generation.replace(".", cls.switch_lang("__", "::", language))
        return generation

    @classmethod
    def is_reference_value(cls, value: str) -> bool:
        return value.startswith("%") and value.endswith("%")

    @classmethod
    def generate_ref_value(cls, value: str, library_name: str, language: str) -> str:
        return cls.construct_type(value[1:-1], library_name, language)

    @classmethod
    def generate_comment(cls, comment: str) -> str:
        return f" /* {comment} */"

    @classmethod
    def generate_fields(
        cls, fields: List[ecoa_types_2_0.Field], library_name: str, language: str, indent_level: int
    ) -> str:
        """Generates fields for a record or a variant record.

        Args:
            - fields

        Returns:
            The generated fields.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        generation = ""
        for field in fields:
            generation += cls.SPACE_INDENTATION[:indent_level]
            generation += f"{cls.construct_type(field.type, library_name, language)} {field.name};"
            if field.comment:
                generation += cls.generate_comment(field.comment)
            generation += cls.LINE_BREAK[:1]
        return generation
