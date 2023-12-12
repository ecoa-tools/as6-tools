# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Simple generation class.
"""

# Standard library imports
import logging

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class SimpleGenerator:
    """"""

    _simple: ecoa_types_2_0.Simple = None
    _library_name: str = None
    _language: str = None
    _indent_level: int = None
    _indent_step: int = None

    def __init__(
        self,
        simple: ecoa_types_2_0.Simple,
        library_name: str,
        language: str,
        indent_level: int,
        indent_step: int,
    ):
        self._simple = simple
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level
        self._indent_step = indent_step

    def _generate_constant_range_value(self, range_value) -> str:
        generation = ""
        if Common.is_reference_value(range_value):
            generation += Common.generate_ref_value(range_value, self._library_name, self._language)
        else:
            generation += range_value
        return generation

    def _generate_simple_comments(self) -> str:
        generation = ""
        if self._simple.comment or self._simple.unit or self._simple.precision:
            generation_com = " /* "
            if self._simple.comment:
                generation_com += f"Comment: {self._simple.comment} "
            if self._simple.unit:
                generation_com += f"Unit: {self._simple.unit} "
            if self._simple.precision:
                generation_com += f"Precision: {self._simple.precision} "
            generation += generation_com + "*/"
        return generation

    def generate(self) -> str:
        """Generates simple types that is a refinement of a basic type with a new name.

        Returns:
            The generated simple types.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        type = Common.construct_type(self._simple.type, self._library_name, self._language)
        generation = (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "typedef "
            + type
            + Common.SPACE_INDENTATION[1]
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._simple.name
            + ";"
        )
        # Generating comments
        generation += self._generate_simple_comments() + Common.LINE_BREAK[:1]
        # Generating minimum range value
        if self._simple.min_range:
            generation += Common.SPACE_INDENTATION[: self._indent_level]
            generation += Common.switch_lang(
                f"#define {self._library_name}__{self._simple.name}_minRange (",
                f"static const {type} {self._simple.name}_minRange = ",
                self._language,
            )
            generation += self._generate_constant_range_value(self._simple.min_range)
            generation += (
                Common._constant_suffixes.get(self._simple.type, "")
                + Common.switch_lang(")", ";", self._language)
                + Common.LINE_BREAK[:1]
            )
        # Generating maximum range value
        if self._simple.max_range:
            generation += Common.SPACE_INDENTATION[: self._indent_level]
            generation += Common.switch_lang(
                f"#define {self._library_name}__{self._simple.name}_maxRange (",
                f"static const {type} {self._simple.name}_maxRange = ",
                self._language,
            )
            generation += self._generate_constant_range_value(self._simple.max_range)
            generation += (
                Common._constant_suffixes.get(self._simple.type, "")
                + Common.switch_lang(")", ";", self._language)
                + Common.LINE_BREAK[:1]
            )
        return generation
