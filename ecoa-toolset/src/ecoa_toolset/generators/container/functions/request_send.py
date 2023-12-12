# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Request Send generation class.
"""

from typing import Dict

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import RequestReceived, RequestSend, Variable


class RequestSendGenerator(FunctionGenerator):
    """"""

    unit_test: bool = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, unit_test: bool):
        super().__init__(indent_level, indent_step, body)
        self.unit_test = unit_test

    def _generate_context_argument(self, element: RequestSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + "__context * context"
            + (
                ","
                if not element.is_synchronous or element.inputs or (element.is_synchronous and element.outputs)
                else ""
            )
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_id_argument(self, element: RequestSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 "
            + Common.switch_lang("*", "&", element.language)
            + " ID"
            + ("," if element.inputs or (element.is_synchronous and element.outputs) else "")
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_prototype(self, element: RequestSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += (
            element.name + "__request_" + ("sync" if element.is_synchronous else "async") + " (" + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        if element.language == "c":
            generation += self._generate_context_argument(element)
        if not element.is_synchronous:
            generation += self._generate_id_argument(element)
        generation += Common.generate_function_parameters(
            element.inputs, element.language, self.indent_level, last_comma=(element.is_synchronous and element.outputs)
        )
        if element.is_synchronous:
            generation += Common.generate_function_parameters(
                element.outputs, element.language, self.indent_level, is_out=True
            )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body_update_global_variable(self, element: RequestSend) -> str:
        generation = ""
        if element.is_synchronous:
            for parameter in element.outputs:
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + "CM_GLOBAL_"
                    + element.module_impl_name
                    + "__"
                    + element.name
                    + "_"
                    + parameter.name
                    + " = "
                )
                generation += Common.switch_lang("", "&", element.language)
                generation += parameter.name + ";" + Common.LINE_BREAK[:1]
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "CM_GLOBAL_"
            + element.module_impl_name
            + "__"
            + element.name
            + "_RRI_ID = "
            + "CM_GLOBAL_"
            + element.module_impl_name
            + "__"
            + element.name
            + "_RRI_ID + 1;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_body_init_id(self, element: RequestSend) -> str:
        generation = ""
        if element.is_synchronous:
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "ECOA"
                + Common.switch_lang("__", "::", element.language)
                + "uint32 ID;"
                + Common.LINE_BREAK[:1]
            )
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("*" if not element.is_synchronous else "", "", element.language)
            + "ID = (ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint16) "
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->mod_id;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("*" if not element.is_synchronous else "", "", element.language)
            + "ID |= "
            + "CM_GLOBAL_"
            + element.module_impl_name
            + "__"
            + element.name
            + "_RR_ID << 16;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("*" if not element.is_synchronous else "", "", element.language)
            + "ID |= "
            + "CM_GLOBAL_"
            + element.module_impl_name
            + "__"
            + element.name
            + "_RRI_ID << 24;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_request_received_id_argument(self, element: RequestSend, receiver: RequestReceived) -> str:
        cast = ""
        if element.language == "c" and receiver.language == "c++":
            cast += "(const ECOA::uint32) "
        elif element.language == "c++" and receiver.language == "c":
            cast += "(const ECOA__uint32) "
        return cast + ("" if element.language == "c++" or element.is_synchronous else "*") + "ID"

    def _generate_request_received_argument(
        self, element: RequestSend, receiver: RequestReceived, argument: Variable, index: int
    ) -> str:
        parameters_used = set()
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        if argument.name == "ID":
            generation += self._generate_request_received_id_argument(element, receiver)
        else:
            argument_found = next(
                (
                    v
                    for v in element.inputs
                    if Common.construct_complete_variable_type(v, element.language)
                    == Common.construct_complete_variable_type(argument, element.language)
                ),
                None,
            )
            if argument_found:
                generation += Common.cast_argument(element, receiver, argument_found)
                parameters_used.add(argument_found.namespace + ":" + argument_found.type + ":" + argument_found.name)
        generation += ("" if index == len(receiver.inputs) - 1 else ",") + Common.LINE_BREAK[:1]
        return generation, parameters_used

    def _generate_request_received_call(
        self,
        element: RequestSend,
        receiver: RequestReceived,
        module_inst_name_receiver: str,
        component_name_receiver: str,
    ) -> str:
        parameters_used = set()
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            receiver.module_impl_name + "__",
            module_inst_name_receiver + "_" + component_name_receiver + "_Module.",
            receiver.language,
        )
        generation += receiver.name + "__request_received (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if receiver.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "&"
                + module_inst_name_receiver
                + "_"
                + component_name_receiver
                + "_Context"
                + ("," if receiver.inputs else "")
                + Common.LINE_BREAK[:1]
            )
        for index, argument in enumerate(receiver.inputs):
            tmp = self._generate_request_received_argument(element, receiver, argument, index)
            generation += tmp[0]
            parameters_used |= tmp[1]
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ");" + Common.LINE_BREAK[:1]
        return generation, parameters_used

    def _generate_request_received_calls(self, element: RequestSend, receivers: Dict) -> str:
        parameters_used = set()
        generation = ""
        for key_receiver, receiver in receivers.items():
            module_inst_name_receiver, component_name_receiver = tuple(key_receiver.split(":"))
            tmp = self._generate_request_received_call(
                element,
                receiver,
                module_inst_name_receiver,
                component_name_receiver,
            )
            generation += tmp[0]
            parameters_used |= tmp[1]
        return generation, parameters_used

    def _generate_else_statement(self, element: RequestSend) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "else"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_", "::", element.language)
            + ("NO_RESPONSE" if element.is_synchronous else "RESOURCE_NOT_AVAILABLE")
            + ";"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        return generation

    def _generate_return_statement(self, element: RequestSend) -> str:
        return (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )

    def _generate_body(self, element: RequestSend) -> str:
        parameters_used = set()
        generation = self._generate_body_update_global_variable(element)
        generation += self._generate_body_init_id(element)
        if self.unit_test:
            generation += Common.generate_body_unit_test(self.indent_level) + Common.LINE_BREAK[:2]
        else:
            for index, (key_sender, receivers) in enumerate(element.receivers.items()):
                module_inst_name_sender, component_name_sender = tuple(key_sender.split(":"))
                generation += Common.generate_mod_id_if_statement(
                    module_inst_name_sender, component_name_sender, element.language, index, self.indent_level
                )
                self.indent_level += self.indent_step
                tmp = self._generate_request_received_calls(element, receivers)
                generation += tmp[0]
                parameters_used |= tmp[1]
                self.indent_level -= self.indent_step
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
            if element.receivers:
                generation += self._generate_else_statement(element)
            else:
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "/* Does nothing */"
        generation += self._generate_return_statement(element)
        tmp = Common.cast_unused_parameters(element.inputs, parameters_used, self.indent_level)
        generation = tmp + Common.LINE_BREAK[: tmp != ""] + generation
        return generation
