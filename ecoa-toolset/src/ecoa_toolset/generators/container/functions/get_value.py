# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Get Value generation class.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import Property


class GetValueGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: Property) -> str:
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
        generation += "get_" + element.name + "_value (" + Common.LINE_BREAK[:1]
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
            + element.namespace.replace(".", Common.switch_lang("__", "::", element.language))
            + Common.switch_lang("__", "::", element.language)
            + element.type
            + " "
            + Common.switch_lang("*", "&", element.language)
            + " value"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Property) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        if getattr(element.type_category, "is_complex", ""):
            generation += (
                "memcpy("
                + Common.switch_lang("", "&", element.language)
                + "value, &("
                + Common.switch_lang("context->platform_", "this->", element.language)
                + "hook->properties->"
                + element.name
                + "), sizeof("
                + element.namespace.replace(".", Common.switch_lang("__", "::", element.language))
                + Common.switch_lang("__", "::", element.language)
                + element.type
                + "))"
            )
        else:
            generation += (
                Common.switch_lang("*", "", element.language)
                + "value = ("
                + element.namespace.replace(".", Common.switch_lang("__", "::", element.language))
                + Common.switch_lang("__", "::", element.language)
                + element.type
                + ") "
                + Common.switch_lang("context->platform_", "this->", element.language)
                + "hook->properties->"
                + element.name
            )
        generation += ";"
        return generation
