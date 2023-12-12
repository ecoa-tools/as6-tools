# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Pinfo generation classes.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import Pinfo


class ReadGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: Pinfo) -> str:
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
        generation += "read_" + element.name + Common.SPACE_INDENTATION[:1] + "(" + Common.LINE_BREAK[:1]
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
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "byte * memory_address,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 in_size,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 * out_size"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Pinfo) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "if (!memory_address)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            "fclose(context->platform_hook->" + element.name + "->pinfo_file);",
            "this->hook->" + element.name + "->pinfo_file.close();",
            element.language,
        )
        generation += (
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_", "::", element.language)
            + "INVALID_PARAMETER;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            (
                "unsigned int count_elem = fread(memory_address, sizeof(ECOA__byte), in_size, context->platform_hook->"
                + element.name
                + "->pinfo_file);"
            ),
            (
                "this->hook->"
                + element.name
                + "->pinfo_file.read((char*)memory_address, in_size);"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "unsigned int count_elem = this->hook->"
                + element.name
                + "->pinfo_file.gcount();"
            ),
            element.language,
        )
        generation += Common.LINE_BREAK[:2] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            "if ((in_size + context->platform_hook->", "if ((in_size + this->hook->", element.language
        )
        generation += element.name
        generation += Common.switch_lang(
            "->pinfo_index) > context->platform_hook->", "->pinfo_index) > this->hook->", element.language
        )
        generation += (
            element.name
            + "->pinfo_size)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->"
            + element.name
            + "->pinfo_index = "
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->"
            + element.name
            + "->pinfo_size;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "else"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->"
            + element.name
            + "->pinfo_index = "
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->"
            + element.name
            + "->pinfo_index + in_size;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "*out_size = count_elem;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )
        return generation


class SeekGenerator(FunctionGenerator):
    """"""

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)

    def _generate_prototype(self, element: Pinfo) -> str:
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
        generation += "seek_" + element.name + " (" + Common.LINE_BREAK[:1]
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
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "int32 offset,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "seek_whence_type whence,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 * new_position"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Pinfo) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            (
                "int returnCode = fseek(context->platform_hook->"
                + element.name
                + "->pinfo_file, offset, whence);"
                + Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "if (returnCode != 0)"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "{"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + "fclose(context->platform_hook->"
                + element.name
                + "->pinfo_file);"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + "return ECOA__return_status_INVALID_PARAMETER;"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "}"
            ),
            "this->hook->" + element.name + "->pinfo_file.seekg(offset, (std::ios_base::seekdir) ((int) whence));",
            element.language,
        )
        generation += Common.LINE_BREAK[:2] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            (
                "context->platform_hook->"
                + element.name
                + "->pinfo_index = ftell(context->platform_hook->"
                + element.name
                + "->pinfo_file);"
            ),
            "this->hook->" + element.name + "->pinfo_index = this->hook->" + element.name + "->pinfo_file.tellg();",
            element.language,
        )
        generation += Common.LINE_BREAK[:2] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang("if (context->platform_hook->", "if (this->hook->", element.language)
        generation += element.name
        generation += Common.switch_lang(
            "->pinfo_index > context->platform_hook->", "->pinfo_index > this->hook->", element.language
        )
        generation += (
            element.name
            + "->pinfo_size)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            "fclose(context->platform_hook->" + element.name + "->pinfo_file);",
            "this->hook->" + element.name + "->pinfo_file.close();",
            element.language,
        )
        generation += (
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_", "::", element.language)
            + "INVALID_PARAMETER;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "*new_position = "
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->"
            + element.name
            + "->pinfo_index;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )
        return generation


class PinfoGenerator:
    """"""

    read: ReadGenerator = None
    seek: SeekGenerator = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        self.read = ReadGenerator(indent_level, indent_step, body)
        self.seek = SeekGenerator(indent_level, indent_step, body)
