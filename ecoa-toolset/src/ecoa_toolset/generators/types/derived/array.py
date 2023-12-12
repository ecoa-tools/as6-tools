# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Array generation class.
"""

# Standard library imports
import logging
from typing import Union

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class ArrayGenerator:
    """"""

    def __init__(
        self,
        array: Union[ecoa_types_2_0.Array, ecoa_types_2_0.FixedArray],
        library_name: str,
        language: str,
        indent_level: int,
        indent_step: int,
        fixed=False,
    ):
        self._array = array
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level
        self._indent_step = indent_step
        self._fixed = fixed

    def _generate_maxsize(self) -> str:
        generation = Common.SPACE_INDENTATION[: self._indent_level]
        generation += Common.switch_lang(
            f"#define {self._library_name}__{self._array.name}_MAXSIZE ",
            f"static const ECOA::uint32 {self._array.name}_MAXSIZE = ",
            self._language,
        )
        if Common.is_reference_value(self._array.max_number):
            generation += Common.generate_ref_value(self._array.max_number, self._library_name, self._language)
            generation += Common.switch_lang("", ";", self._language)
        else:
            generation += Common.switch_lang(
                f"({self._array.max_number})", f"{self._array.max_number};", self._language
            )
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_array(self) -> str:
        generation = (
            "typedef struct"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self._indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self._indent_level += self._indent_step
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", self._language)
            + "uint32 current_size;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self._indent_level]
            + Common.construct_type(self._array.item_type, self._library_name, self._language)
            + " data["
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._array.name
            + "_MAXSIZE];"
            + Common.LINE_BREAK[:1]
        )
        self._indent_level -= self._indent_step
        generation += (
            Common.SPACE_INDENTATION[: self._indent_level]
            + "} "
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._array.name
            + ";"
        )
        return generation

    def _generate_fixed_array(self) -> str:
        generation = (
            "typedef "
            + Common.construct_type(self._array.item_type, self._library_name, self._language)
            + Common.SPACE_INDENTATION[:1]
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._array.name
            + "["
            + Common.switch_lang(self._library_name + "__", "", self._language)
            + self._array.name
            + "_MAXSIZE];"
        )
        return generation

    def generate(self) -> str:
        """Generates an array or a fixed array that are an ordered collection of elements of the same type.

        Returns:
            The generated array or fixed array.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        generation = self._generate_maxsize()
        generation += Common.SPACE_INDENTATION[: self._indent_level]
        if self._fixed:
            generation += self._generate_fixed_array()
        else:
            generation += self._generate_array()
        if self._array.comment:
            generation += Common.generate_comment(self._array.comment)
        generation += Common.LINE_BREAK[:1]
        return generation
