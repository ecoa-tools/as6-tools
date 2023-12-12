# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Global Variable generation class.
"""

# Internal library imports
from ecoa_toolset.generators.container.common import Common
from ecoa_toolset.generators.helpers.global_variable import CMGlobalVariable


class CMGlobalVariableGenerator:
    """"""

    def generate(self, element: CMGlobalVariable):
        """"""
        generation = (
            Common.construct_complete_variable_type(element, element.language)
            + Common.SPACE_INDENTATION[:1]
            + ("*" + Common.SPACE_INDENTATION[:1] if element.is_out else "")
            + "CM_GLOBAL_"
            + element.name
        )
        if element.value:
            generation += " = " + element.value
        generation += ";" + Common.LINE_BREAK[:1]
        return generation
