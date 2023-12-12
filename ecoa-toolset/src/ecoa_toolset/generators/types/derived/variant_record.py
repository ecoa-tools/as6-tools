# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Variant Record generation class.
"""

# Standard library imports
import logging

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class VariantRecordGenerator:
    """"""

    def __init__(
        self,
        variant: ecoa_types_2_0.VariantRecord,
        library_name: str,
        language: str,
        indent_level: int,
        indent_step: int,
    ):
        self._variant = variant
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level
        self._indent_step = indent_step

    def generate(self) -> str:
        """Generates a type that contains a fixed set of fields, a set of optional fields and a selector.

        Returns:
            The generated variant record.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        generation = (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "typedef struct"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self._indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self._indent_level += self._indent_step
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + Common.construct_type(self._variant.select_type, self._library_name, self._language)
            + " "
            + self._variant.select_name
            + ";"
            + Common.LINE_BREAK[:1]
        )
        generation += Common.generate_fields(
            self._variant.field, self._library_name, self._language, self._indent_level
        )
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "union "
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self._indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self._indent_level += self._indent_step
        generation += Common.generate_fields(
            self._variant.union, self._library_name, self._language, self._indent_level
        )
        self._indent_level -= self._indent_step
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "} u_"
            + self._variant.select_name
            + ";"
            + Common.LINE_BREAK[:1]
        )
        self._indent_level -= self._indent_step
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "} "
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._variant.name
            + ";"
        )
        if self._variant.comment:
            generation += Common.generate_comment(self._variant.comment)
        generation += Common.LINE_BREAK[:1]
        return generation
