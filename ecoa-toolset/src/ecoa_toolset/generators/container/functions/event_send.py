# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Event Send generation class.
"""

from typing import Dict

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import EventSend


class EventSendGenerator(FunctionGenerator):
    """"""

    unit_test: bool = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, unit_test: bool):
        super().__init__(indent_level, indent_step, body)
        self.unit_test = unit_test

    def _generate_prototype(self, element: EventSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += element.name + "__send (" + Common.LINE_BREAK[:1]
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

    def _generate_event_received_calls(self, element: EventSend, receivers: Dict) -> str:
        parameters_used = set()
        generation = ""
        for key_receiver, receiver in receivers.items():
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
        return generation, parameters_used

    def _generate_body(self, element: EventSend) -> str:
        parameters_used = set()
        generation = ""
        if self.unit_test:
            generation += Common.generate_body_unit_test(self.indent_level)
        else:
            for index, (key_sender, receivers) in enumerate(element.receivers.items()):
                module_inst_name_sender, component_name_sender = tuple(key_sender.split(":"))
                generation += Common.LINE_BREAK[: index != 0]
                generation += Common.generate_mod_id_if_statement(
                    module_inst_name_sender, component_name_sender, element.language, index, self.indent_level
                )
                self.indent_level += self.indent_step
                tmp = self._generate_event_received_calls(element, receivers)
                generation += tmp[0]
                parameters_used |= tmp[1]
                self.indent_level -= self.indent_step
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "}"
            if not element.receivers:
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "/* Does nothing */"
        tmp1 = ""
        if self.unit_test or not element.receivers:
            if element.language == "c":
                tmp1 += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
        tmp2 = Common.cast_unused_parameters(element.inputs, parameters_used, self.indent_level)
        generation = tmp1 + tmp2 + Common.LINE_BREAK[: tmp2 != ""] + generation
        return generation
