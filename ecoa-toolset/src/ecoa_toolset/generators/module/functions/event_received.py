# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Event Received generation class.
"""

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.generators.module.common import Common
from ecoa_toolset.models.components import EventReceived, Parameter
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class EventReceivedGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: EventReceived) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "__", "Module::" if self.body else "", element.language
        )
        generation += element.name + "__received (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if element.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + element.module_impl_name
                + "__context * context"
                + ("," if element.inputs else "")
                + Common.LINE_BREAK[:1]
            )
        generation += Common.generate_function_parameters(element.inputs, element.language, self.indent_level)
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: EventReceived) -> str:
        generation = ""
        if element.language == "c":
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
        generation += Common.cast_unused_parameters(element.inputs, set(), self.indent_level)
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "// Insert logic here."
        return generation

    def generate(self, element: EventReceived) -> str:
        """"""
        generation = ""
        if self.body:
            arguments = [argument for argument in element.inputs]
            if element.language == "c":
                arguments = [
                    Parameter("context", element.module_impl_name, "context", ecoa_types_2_0.Record)
                ] + arguments
            generation += Common.generate_function_header_comment(arguments)
        generation += super().generate(element)
        return generation
