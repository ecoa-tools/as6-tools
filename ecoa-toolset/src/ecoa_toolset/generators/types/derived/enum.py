# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Enum generation class.
"""

# Standard library imports
import logging

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class EnumGenerator:
    """"""

    _enum: ecoa_types_2_0.Enum = None
    _library_name: str = None
    _language: str = None
    _indent_level: int = None
    _indent_step: int = None
    _types_helper = None

    def __init__(
        self,
        enum: ecoa_types_2_0.Enum,
        library_name: str,
        language: str,
        indent_level: int,
        indent_step: int,
        types_helper,
    ):
        self._enum = enum
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level
        self._indent_step = indent_step
        self._types_helper = types_helper

    def _find_reference_value(self, reference: str) -> str:
        type_category = self._types_helper.get_type_category(self._types_helper.add_namespace(reference[1:-1]))
        if Common.is_reference_value(type_category.value):
            return self._find_reference_value(type_category.value)
        return type_category.value

    def _generate_enum_value_and_update_default_value(self, value: ecoa_types_2_0.EnumValue, default_value: str) -> str:
        if value.valnum:
            if Common.is_reference_value(value.valnum):
                real_value = Common.generate_ref_value(value.valnum, self._library_name, self._language)
                default_value = self._find_reference_value(value.valnum)
            else:
                default_value = real_value = value.valnum
        else:
            real_value = default_value
        if default_value.isdigit():
            default_value = str(int(default_value) + 1)
        elif len(default_value) == 1:
            default_value = chr(ord(default_value) + 1)
        if not real_value.isdigit() and len(real_value) == 1:
            real_value = f"'{real_value[0]}'"
        return real_value, default_value

    def _generate_enum_value(self) -> str:
        generation = ""
        default_value = "0"
        for value in self._enum.value:
            generation += Common.switch_lang(
                f"#define {self._library_name}__{self._enum.name}_{value.name} (",
                f"{Common.SPACE_INDENTATION[: (self._indent_level + 2 * self._indent_step)]}{value.name} = ",
                self._language,
            )
            real_value, default_value = self._generate_enum_value_and_update_default_value(value, default_value)
            generation += real_value + Common.switch_lang(")", ",", self._language)
            if value.comment:
                generation += Common.generate_comment(value.comment)
            generation += Common.LINE_BREAK[:1]
        return generation

    def generate(self) -> str:
        """Generates enumeration types that defines a set of labels.

        Returns:
            The generated enums.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        type = Common.construct_type(self._enum.type, self._library_name, self._language)
        generation = Common.SPACE_INDENTATION[: self._indent_level]
        generation += Common.switch_lang(
            "typedef",
            (
                "struct "
                + self._enum.name
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self._indent_level]
                + "{"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + type
                + " value;"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "enum EnumValues"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "{"
                + Common.LINE_BREAK[:1]
                + self._generate_enum_value()
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "};"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "inline void operator = ("
                + type
                + " i) { value = i; }"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "inline operator"
            ),
            self._language,
        )
        generation += f" {type} "
        generation += Common.switch_lang(
            self._library_name + "__",
            (
                "() const { return value; }"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "inline "
                + self._enum.name
                + " (EnumValues v):value(v) {}"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self._indent_level + self._indent_step)]
                + "inline "
            ),
            self._language,
        )
        generation += self._enum.name
        if self._language == "c++":
            generation += (
                " ():value("
                + self._enum.value[0].name
                + ") {}"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self._indent_level]
                + "}"
            )
        generation += ";"
        if self._enum.comment:
            generation += Common.generate_comment(self._enum.comment)
        generation += Common.LINE_BREAK[:1] + Common.switch_lang(self._generate_enum_value(), "", self._language)
        return generation
