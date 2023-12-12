# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""External generation class.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import External


class ExternalGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: External) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.component_impl_name + "__",
            element.component_impl_name + "_External_Interface::" if self.body else "",
            element.language,
        )
        generation += element.name + " (" + Common.LINE_BREAK[:1]
        generation += Common.generate_function_parameters(
            element.inputs, element.language, self.indent_level + self.indent_step
        )
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: External) -> str:
        parameters_used = set()
        generation = ""
        for key_receiver, receiver in element.receivers.items():
            module_inst_name_receiver, component_name_receiver = tuple(key_receiver.split(":"))
            tmp = Common.generate_event_received_call(
                element,
                receiver,
                module_inst_name_receiver,
                component_name_receiver,
                self.indent_level,
                self.indent_step,
            )
            generation += tmp[0]
            parameters_used |= tmp[1]
        if not element.receivers:
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "/* Does nothing */"
        tmp = Common.cast_unused_parameters(element.inputs, parameters_used, self.indent_level)
        generation = tmp + Common.LINE_BREAK[: tmp != ""] + generation
        return generation
