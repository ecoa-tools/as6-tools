# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Save Warm Start Context generation class.
"""

from typing import Tuple

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator


class SaveWarmStartContextGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: Tuple) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element[0] + "_container__",
            element[0] + "::Container::" if self.body else "",
            element[1],
        )
        generation += "save_warm_start_context (" + Common.LINE_BREAK[:1]
        if element[1] == "c":
            generation += (
                Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + element[0]
                + "__context * context"
                + Common.LINE_BREAK[:1]
            )
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Tuple) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        if element[1] == "c":
            generation += "(void) context;" + Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += 'printf("Saving warm start context of ' + element[0] + '\\n");'
        return generation
