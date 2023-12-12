# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Constant generation class.
"""

# Standard library imports
import logging

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class ConstantGenerator:
    """"""

    def __init__(
        self,
        constant: ecoa_types_2_0.Constant,
        library_name: str,
        language: str,
        indent_level: int,
    ):
        self._constant = constant
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level

    def generate(self) -> str:
        """Generates a constant variable.

        Returns:
            The generated constant.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        logger.debug(f"{Common.TAB_INDENTATION[:2]}{self._constant.name}")
        generation = Common.SPACE_INDENTATION[: self._indent_level]
        generation += Common.switch_lang(
            f"#define {self._library_name}__{self._constant.name} (",
            (
                f"static const {Common.construct_type(self._constant.type, self._library_name, self._language)}"
                + f" {self._constant.name} = "
            ),
            self._language,
        )
        if Common.is_reference_value(self._constant.value):
            generation += Common.generate_ref_value(self._constant.value, self._library_name, self._language)
        else:
            if not self._constant.value.isdigit() and len(self._constant.value) == 1:
                generation += f"'{self._constant.value[0]}'"
            else:
                generation += self._constant.value
        generation += Common._constant_suffixes.get(self._constant.type, "")
        generation += Common.switch_lang(")", ";", self._language)
        if self._constant.comment:
            generation += Common.generate_comment(self._constant.comment)
        generation += Common.LINE_BREAK[:1]
        return generation
