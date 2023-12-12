# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Response Received generation class.
"""

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.generators.module.common import Common
from ecoa_toolset.models.components import Parameter, RequestSend
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class ResponseReceivedGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: RequestSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "__", "Module::" if self.body else "", element.language
        )
        generation += element.name + "__response_received (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if element.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + element.module_impl_name
                + "__context * context,"
                + Common.LINE_BREAK[:1]
            )
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "const ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 ID,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "const ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status status"
            + ("," if element.outputs else "")
            + Common.LINE_BREAK[:1]
        )
        generation += Common.generate_function_parameters(element.outputs, element.language, self.indent_level)
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: RequestSend) -> str:
        generation = ""
        if element.language == "c":
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) ID;" + Common.LINE_BREAK[:1]
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) status;" + Common.LINE_BREAK[:1]
        generation += Common.cast_unused_parameters(element.outputs, set(), self.indent_level)
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "// Insert logic here."
        return generation

    def generate(self, element: RequestSend) -> str:
        """"""
        generation = ""
        if self.body:
            arguments = [
                Parameter("ID", "ECOA", "uint32", ecoa_types_2_0.Simple),
                Parameter("status", "ECOA", "return_status", ecoa_types_2_0.Enum),
            ]
            if element.language == "c":
                arguments = [
                    Parameter("context", element.module_impl_name, "context", ecoa_types_2_0.Record)
                ] + arguments
            generation += Common.generate_function_header_comment(arguments)
        generation += super().generate(element)
        return generation
