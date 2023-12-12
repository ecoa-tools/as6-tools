# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Logs generation class.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import Log, LogType


class LogsGenerator(FunctionGenerator):
    """"""

    log_level: int = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: Log) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level] + "void" + Common.LINE_BREAK[:1]
        generation += Common.SPACE_INDENTATION[: self.indent_level] + Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += self.log_level.name.lower() + " (" + Common.LINE_BREAK[:1]
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
            + "log"
            + Common.switch_lang(" ", " & ", element.language)
            + "log"
        )
        if self.log_level in [LogType.RAISE_ERROR, LogType.RAISE_FATAL_ERROR]:
            generation += (
                ","
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "const ECOA"
                + Common.switch_lang("__", "::", element.language)
                + "error_code error_code"
            )
        self.indent_level -= self.indent_step
        generation += Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Log) -> str:
        generation = ""
        if element.language == "c":
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
        if self.log_level in [LogType.RAISE_ERROR, LogType.RAISE_FATAL_ERROR]:
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) error_code;" + Common.LINE_BREAK[:1]
        generation += Common.SPACE_INDENTATION[: self.indent_level] + 'printf("[\\x1B['
        if self.log_level == LogType.LOG_WARNING:
            generation += "33"
        elif self.log_level == LogType.RAISE_ERROR:
            generation += "31"
        elif self.log_level == LogType.RAISE_FATAL_ERROR:
            generation += "41"
        else:
            generation += "32"
        generation += "m" + "_".join(self.log_level.name.split("_")[1:]) + '\\x1B[39m] %s\\n", log.data);'
        return generation

    def generate(self, element: Log) -> str:
        """"""
        generation = ""
        for log_level in LogType:
            self.log_level = log_level
            generation += super().generate(element)
        return generation
