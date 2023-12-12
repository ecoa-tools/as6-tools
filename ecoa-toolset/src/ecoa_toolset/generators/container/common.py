# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Common attributes for container code generation.
"""

from typing import Any

# Internal library imports
from ecoa_toolset.generators.common import Common as GlobalCommon
from ecoa_toolset.models.components import EventReceived, Variable
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class Common(GlobalCommon):
    """Common attributes."""

    @classmethod
    def cast_enum_c_to_cpp(cls, argument: Variable):
        argument_complete_type = f'{argument.namespace.replace(".", "::")}::{argument.type}'
        return f"{argument_complete_type}(({argument_complete_type}::EnumValues) {argument.name})"

    @classmethod
    def cast_enum_cpp_to_c(cls, argument: Variable):
        argument_complete_type = f'{argument.namespace.replace(".", "__")}__{argument.type}'
        return f"({argument_complete_type}) {argument.name}"

    @classmethod
    def cast_enum(cls, element: Any, other: Any, argument: Variable):
        """"""
        generation = ""
        if element.language == "c" and other.language == "c++":
            generation += cls.cast_enum_c_to_cpp(argument)
        elif element.language == "c++" and other.language == "c":
            generation += cls.cast_enum_cpp_to_c(argument)
        else:
            generation += argument.name
        return generation

    @classmethod
    def cast_type_c_to_cpp(cls, argument: Variable):
        """"""
        cast_begin = "("
        argument_complete_type = f'{argument.namespace.replace(".", "::")}::{argument.type}'
        cast_end = "&)*" if getattr(argument.type_category, "is_complex", "") else ")"
        return f"{cast_begin}{argument_complete_type}{cast_end} "

    @classmethod
    def cast_type_cpp_to_c(cls, argument: Variable):
        """"""
        cast_begin = "("
        argument_complete_type = f'{argument.namespace.replace(".", "__")}__{argument.type}'
        cast_end = "*)&" if getattr(argument.type_category, "is_complex", "") else ")"
        return f"{cast_begin}{argument_complete_type}{cast_end} "

    @classmethod
    def cast_type(cls, element: Any, other: Any, argument: Variable):
        """"""
        generation = ""
        if element.language == "c" and other.language == "c++":
            generation += cls.cast_type_c_to_cpp(argument)
        elif element.language == "c++" and other.language == "c":
            generation += cls.cast_type_cpp_to_c(argument)
        generation += argument.name
        return generation

    @classmethod
    def cast_argument(cls, element: Any, other: Any, argument: Variable):
        """"""
        generation = ""
        if isinstance(argument.type_category, ecoa_types_2_0.Enum):
            generation += cls.cast_enum(element, other, argument)
        else:
            generation += cls.cast_type(element, other, argument)
        return generation

    @classmethod
    def _generate_event_received_argument(
        cls, sender: Any, receiver: EventReceived, argument: Variable, index: int, indent_level: int
    ):
        parameters_used = set()
        generation = ""
        argument_found = next(
            (
                v
                for v in sender.inputs
                if cls.construct_complete_variable_type(v, sender.language)
                == cls.construct_complete_variable_type(argument, sender.language)
            ),
            None,
        )
        if argument_found:
            generation += (
                cls.SPACE_INDENTATION[:indent_level]
                + cls.cast_argument(sender, receiver, argument_found)
                + ("" if index == len(receiver.inputs) - 1 else ",")
                + cls.LINE_BREAK[:1]
            )
            parameters_used.add(argument_found.namespace + ":" + argument_found.type + ":" + argument_found.name)
        return generation, parameters_used

    @classmethod
    def generate_event_received_call(
        cls,
        sender: Any,
        receiver: EventReceived,
        module_inst_name_receiver: str,
        component_name_receiver: str,
        indent_level: int,
        indent_step: int,
    ) -> str:
        """"""
        parameters_used = set()
        generation = cls.SPACE_INDENTATION[:indent_level]
        generation += cls.switch_lang(
            receiver.module_impl_name + "__",
            module_inst_name_receiver + "_" + component_name_receiver + "_Module.",
            receiver.language,
        )
        generation += receiver.name + "__received (" + cls.LINE_BREAK[:1]
        indent_level += indent_step
        if receiver.language == "c":
            generation += (
                cls.SPACE_INDENTATION[:indent_level]
                + "&"
                + module_inst_name_receiver
                + "_"
                + component_name_receiver
                + "_Context"
                + ("," if receiver.inputs else "")
                + cls.LINE_BREAK[:1]
            )
        for index, argument in enumerate(receiver.inputs):
            tmp = cls._generate_event_received_argument(sender, receiver, argument, index, indent_level)
            generation += tmp[0]
            parameters_used |= tmp[1]
        indent_level -= indent_step
        generation += cls.SPACE_INDENTATION[:indent_level] + ");" + cls.LINE_BREAK[:1]
        return generation, parameters_used

    @classmethod
    def generate_mod_id_if_statement(
        cls, module_inst_name: str, component_name: str, language: str, index: int, indent_level: int
    ) -> str:
        """"""
        generation = (
            cls.SPACE_INDENTATION[:indent_level]
            + ("if" if index == 0 else "else if")
            + " ("
            + cls.switch_lang("context->platform_", "this->", language)
            + "hook->mod_id == "
            + module_inst_name.upper()
            + "_"
            + component_name.upper()
            + "_ID)"
            + cls.LINE_BREAK[:1]
            + cls.SPACE_INDENTATION[:indent_level]
            + "{"
            + cls.LINE_BREAK[:1]
        )
        return generation

    @classmethod
    def generate_body_unit_test(cls, indent_level: int) -> str:
        """"""
        return Common.SPACE_INDENTATION[:indent_level] + "// Insert logic here."
