# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Response Send generation class.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import RequestReceived, RequestSend, Variable


class ResponseSendGenerator(FunctionGenerator):
    """"""

    unit_test: bool = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, unit_test: bool):
        super().__init__(indent_level, indent_step, body)
        self.unit_test = unit_test

    def _generate_prototype(self, element: RequestReceived) -> str:
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
        generation += element.name + "__response_send (" + Common.LINE_BREAK[:1]
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
            + "uint32 ID"
            + ("," if element.outputs else "")
            + Common.LINE_BREAK[:1]
        )
        generation += Common.generate_function_parameters(element.outputs, element.language, self.indent_level)
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_sender_mod_id(self, element: RequestReceived) -> str:
        return (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint16 sender_mod_id = (ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint16)(ID & 0xffffU);"
            + Common.LINE_BREAK[:2]
        )

    def _generate_if_statement(
        self,
        module_inst_name_receiver: str,
        component_name_receiver: str,
        module_inst_name_sender: str,
        component_name_sender: str,
        language: str,
        index: int,
    ) -> str:
        return (
            Common.SPACE_INDENTATION[: self.indent_level]
            + ("if" if index == 0 else "else if")
            + " ("
            + Common.switch_lang("context->platform_", "this->", language)
            + "hook->mod_id == "
            + module_inst_name_receiver.upper()
            + "_"
            + component_name_receiver.upper()
            + "_ID && sender_mod_id == "
            + module_inst_name_sender.upper()
            + "_"
            + component_name_sender.upper()
            + "_ID)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )

    def _generate_memcpy_call_cast_c_to_cpp(self, parameter: Variable) -> str:
        generation = (
            "("
            + parameter.namespace.replace(".", "::")
            + "::"
            + parameter.type
            + " *) "
            + ("&" if not getattr(parameter.type_category, "is_complex", "") else "")
        )
        return generation

    def _generate_memcpy_call_cast_cpp_to_c(self, parameter: Variable) -> str:
        return "(" + parameter.namespace.replace(".", "__") + "__" + parameter.type + " *) &"

    def _generate_memcpy_call(
        self, element: RequestReceived, sender: RequestSend, parameter: Variable, parameter_sender: Variable
    ) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "memcpy(CM_GLOBAL_"
            + sender.module_impl_name
            + "__"
            + sender.name
            + "_"
            + parameter_sender.name
            + ", "
        )
        if element.language == "c" and sender.language == "c++":
            generation += self._generate_memcpy_call_cast_c_to_cpp(parameter)
        elif element.language == "c++" and sender.language == "c":
            generation += self._generate_memcpy_call_cast_cpp_to_c(parameter)
        else:
            generation += (
                "&" if sender.language == "c++" or not getattr(parameter.type_category, "is_complex", "") else ""
            )
        generation += (
            parameter.name
            + ", sizeof("
            + parameter.namespace.replace(".", Common.switch_lang("__", "::", sender.language))
            + Common.switch_lang("__", "::", sender.language)
            + parameter.type
            + "));"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_memcpy_calls(
        self,
        element: RequestReceived,
        sender: RequestSend,
    ) -> str:
        parameters_used = set()
        generation = ""
        for parameter in element.outputs:
            parameter_sender = next(
                (
                    v
                    for v in sender.outputs
                    if Common.construct_complete_variable_type(v, element.language)
                    == Common.construct_complete_variable_type(parameter, element.language)
                ),
                None,
            )
            if parameter_sender:
                generation += self._generate_memcpy_call(element, sender, parameter, parameter_sender)
                parameters_used.add(parameter.namespace + ":" + parameter.type + ":" + parameter.name)
        return generation, parameters_used

    def _generate_response_received_argument(
        self, element: RequestReceived, sender: RequestSend, parameter: Variable, index: int
    ) -> str:
        parameters_used = set()
        generation = ""
        parameter_found = next(
            (
                v
                for v in element.outputs
                if Common.construct_complete_variable_type(v, element.language)
                == Common.construct_complete_variable_type(parameter, element.language)
            ),
            None,
        )
        if parameter_found:
            parameters_used.add(parameter_found.namespace + ":" + parameter_found.type + ":" + parameter_found.name)
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + Common.cast_argument(element, sender, parameter_found)
                + ("" if index == len(sender.outputs) - 1 else ",")
                + Common.LINE_BREAK[:1]
            )
        return generation, parameters_used

    def _generate_response_received_call(
        self,
        element: RequestReceived,
        sender: RequestSend,
        module_inst_name_sender: str,
        component_name_sender: str,
    ) -> str:
        parameters_used = set()
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            sender.module_impl_name + "__",
            module_inst_name_sender + "_" + component_name_sender + "_Module.",
            sender.language,
        )
        generation += sender.name + "__response_received (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if sender.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "&"
                + module_inst_name_sender
                + "_"
                + component_name_sender
                + "_Context,"
                + Common.LINE_BREAK[:1]
            )
        cast = ""
        if element.language == "c" and sender.language == "c++":
            cast += "(const ECOA::uint32) "
        elif element.language == "c++" and sender.language == "c":
            cast += "(const ECOA__uint32) "
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ID,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += (
            "ECOA"
            + Common.switch_lang("__", "::", sender.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", sender.language)
        )
        generation += ("," if sender.outputs else "") + Common.LINE_BREAK[:1]
        for index, parameter in enumerate(sender.outputs):
            tmp = self._generate_response_received_argument(element, sender, parameter, index)
            generation += tmp[0]
            parameters_used |= tmp[1]
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ");" + Common.LINE_BREAK[:1]
        return generation, parameters_used

    def _generate_body_core(
        self,
        element: RequestReceived,
        module_inst_name_receiver: str,
        component_name_receiver: str,
        sender: RequestSend,
        module_inst_name_sender: str,
        component_name_sender: str,
        index: int,
    ) -> str:
        parameters_used = set()
        generation = self._generate_if_statement(
            module_inst_name_receiver,
            component_name_receiver,
            module_inst_name_sender,
            component_name_sender,
            element.language,
            index,
        )
        self.indent_level += self.indent_step
        if sender.is_synchronous:
            tmp = self._generate_memcpy_calls(element, sender)
            generation += tmp[0]
            parameters_used |= tmp[1]
        else:
            tmp = self._generate_response_received_call(
                element,
                sender,
                module_inst_name_sender,
                component_name_sender,
            )
            generation += tmp[0]
            parameters_used |= tmp[1]
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
        return generation, parameters_used

    def _generate_else_statement(self, element: RequestReceived) -> str:
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
            + "INVALID_IDENTIFIER;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        return generation

    def _generate_return_statement(self, element: RequestReceived) -> str:
        return (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )

    def _generate_body(self, element: RequestReceived) -> str:
        parameters_used = set()
        generation = ""
        if self.unit_test:
            generation += Common.generate_body_unit_test(self.indent_level) + Common.LINE_BREAK[:2]
        else:
            if element.senders:
                generation += self._generate_sender_mod_id(element)
            for index1, (key_receiver, senders) in enumerate(element.senders.items()):
                module_inst_name_receiver, component_name_receiver = tuple(key_receiver.split(":"))
                for index2, (key_sender, sender) in enumerate(senders.items()):
                    module_inst_name_sender, component_name_sender = tuple(key_sender.split(":"))
                    tmp = self._generate_body_core(
                        element,
                        module_inst_name_receiver,
                        component_name_receiver,
                        sender,
                        module_inst_name_sender,
                        component_name_sender,
                        index1 + index2,
                    )
                    generation += tmp[0]
                    parameters_used |= tmp[1]
            if element.senders:
                generation += self._generate_else_statement(element)
            else:
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "/* Does nothing */"
        generation += self._generate_return_statement(element)
        tmp1 = ""
        if self.unit_test or not element.senders:
            if element.language == "c":
                tmp1 += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
            tmp1 += Common.SPACE_INDENTATION[: self.indent_level] + "(void) ID;" + Common.LINE_BREAK[:1]
        tmp2 = Common.cast_unused_parameters(element.outputs, parameters_used, self.indent_level)
        generation = tmp1 + tmp2 + Common.LINE_BREAK[: tmp2 != ""] + generation
        return generation
