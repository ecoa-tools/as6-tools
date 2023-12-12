# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Record generation class.
"""

# Standard library imports
import logging

# Internal library imports
from ecoa_toolset.generators.types.derived.common import Common
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0

logger = logging.getLogger(__name__)


class RecordGenerator:
    """"""

    def __init__(
        self, record: ecoa_types_2_0.Record, library_name: str, language: str, indent_level: int, indent_step: int
    ):
        self._record = record
        self._library_name = library_name
        self._language = language
        self._indent_level = indent_level
        self._indent_step = indent_step

    def generate(self) -> str:
        """Generates a type that contains a fixed set of fields of given types.

        Returns:
            The generated record.

        Comments:
            cf. ECOA Architecture Specification Part 4: Software Interface
        """
        logger.debug(f"{Common.TAB_INDENTATION[:1]}Generating records")
        generation = f"{Common.SPACE_INDENTATION[: self._indent_level]}typedef struct{Common.LINE_BREAK[:1]}"
        generation += Common.SPACE_INDENTATION[: self._indent_level] + "{" + Common.LINE_BREAK[:1]
        generation += Common.generate_fields(
            self._record.field, self._library_name, self._language, self._indent_level + self._indent_step
        )
        generation += Common.SPACE_INDENTATION[: self._indent_level] + "} "
        generation += Common.switch_lang(self._library_name + "__", "", self._language) + self._record.name + ";"
        if self._record.comment:
            generation += Common.generate_comment(self._record.comment)
        generation += Common.LINE_BREAK[:1]
        return generation
