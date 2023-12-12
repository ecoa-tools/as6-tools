# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Common attributes for module code generation.
"""

from typing import List

# Internal library imports
from ecoa_toolset.generators.common import Common as GlobalCommon


class Common(GlobalCommon):
    """Common attributes."""

    @classmethod
    def generate_function_header_comment(cls, parameters: List) -> str:
        generation = (
            "/**"
            + Common.LINE_BREAK[:1]
            + " * @internal"
            + Common.SPACE_INDENTATION[:4]
            + "Insert function description here."
            + Common.LINE_BREAK[:1]
        )
        for parameter in parameters:
            generation += (
                " * @param[in]"
                + Common.SPACE_INDENTATION[:3]
                + parameter.name
                + " Insert variable description here."
                + Common.LINE_BREAK[:1]
            )
        generation += " */" + Common.LINE_BREAK[:1]
        return generation
