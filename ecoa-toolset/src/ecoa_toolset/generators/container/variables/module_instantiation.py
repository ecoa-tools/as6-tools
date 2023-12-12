# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module Instantiation generation class.
"""

# Standard library imports
import os
from typing import List

# Internal library imports
from ecoa_toolset.generators.container.common import Common
from ecoa_toolset.generators.helpers.platform_hook import PlatformHook
from ecoa_toolset.generators.helpers.property_value import PropertyValueHelper


class ModuleInstantiationGenerator:
    """"""

    indent_level: int = None
    indent_step: int = None
    visited: List = None
    property_value_helper = None

    def __init__(self, indent_level: int, indent_step: int):
        self.indent_level = indent_level
        self.indent_step = indent_step
        self.visited = []

    def _generate_properties_struct_init(self, element: PlatformHook) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "struct"
            + Common.SPACE_INDENTATION[:1]
            + element.module_impl_name
            + "__properties {"
        )
        self.indent_level += self.indent_step
        for property in element.properties:
            generation += (
                Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + property.namespace.replace(".", Common.switch_lang("__", "::", element.language))
                + Common.switch_lang("__", "::", element.language)
                + property.type
                + Common.SPACE_INDENTATION[:1]
                + property.name
                + ";"
            )
        self.indent_level -= self.indent_step
        generation += (
            Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_properties_struct(self, element: PlatformHook, component_name: str, types_helper) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "struct"
            + Common.SPACE_INDENTATION[:1]
            + element.module_impl_name
            + "__properties"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_properties = {"
        )
        self.indent_level += self.indent_step
        for i, property in enumerate(element.properties):
            property_value = self.property_value_helper.convert(
                property.values.get(
                    property.component_impl_name + ":" + element.module_inst_name + ":" + component_name
                ),
                property.type_category,
                types_helper,
            )
            if property_value:
                generation += (
                    Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + property_value
                    + ("," if i + 1 != len(element.properties) else "")
                    + Common.SPACE_INDENTATION[:1]
                    + "/*"
                    + Common.SPACE_INDENTATION[:1]
                    + property.name
                    + Common.SPACE_INDENTATION[:1]
                    + "*/"
                )
        self.indent_level -= self.indent_step
        generation += (
            Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_pinfo_struct_init(self, element: PlatformHook) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "struct"
            + Common.SPACE_INDENTATION[:1]
            + element.module_impl_name
            + "_pinfo_struct {"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint32 pinfo_index;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("unsigned int", "std::streampos", element.language)
            + " pinfo_size;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + Common.switch_lang("FILE *", "std::ifstream &", element.language)
            + " pinfo_file;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        return generation

    def _generate_pinfo_files(self, element: PlatformHook) -> str:
        generation = ""
        for pinfo in element.pinfos:
            for key, pinfo_file_path in pinfo.values.items():
                module_instance_name, component_name = tuple(key.split(":")[-2:])
                name = module_instance_name + "_" + component_name + "_file_" + pinfo.name
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + "std::ifstream "
                    + name
                    + '("'
                    + Common.replace_escape_string(os.path.abspath(pinfo_file_path))
                    + '", std::ios::binary);'
                    + Common.LINE_BREAK[:1]
                )
        generation += Common.LINE_BREAK[:2]
        return generation

    def _generate_pinfo_struct(self, element: PlatformHook, component_name: str) -> str:
        generation = ""
        for pinfo in element.pinfos:
            pinfo_file_path = pinfo.values.get(
                element.component_impl_name + ":" + element.module_inst_name + ":" + component_name
            )
            pinfo_file_stat = os.stat(pinfo_file_path)
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "struct"
                + Common.SPACE_INDENTATION[:1]
                + element.module_impl_name
                + "_pinfo_struct"
                + Common.SPACE_INDENTATION[:1]
                + element.module_inst_name
                + "_"
                + component_name
                + "_pinfo_struct_"
                + pinfo.name
                + " = {"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level += self.indent_step
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "0,"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + str(pinfo_file_stat.st_size)
                + ","
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
            )
            generation += Common.switch_lang(
                "0",
                element.module_inst_name + "_" + component_name + "_file_" + pinfo.name,
                element.language,
            )
            generation += Common.LINE_BREAK[:1]
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        return generation

    def _generate_platform_hook_struct_init(self, element: PlatformHook) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "struct"
            + Common.SPACE_INDENTATION[:1]
            + element.module_impl_name
            + Common.switch_lang("__", "::Container::", element.language)
            + "platform_hook {"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "uint16 mod_id;"
            + Common.LINE_BREAK[:1]
        )
        if element.properties:
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "struct"
                + Common.SPACE_INDENTATION[:1]
                + element.module_impl_name
                + "__properties * properties;"
                + Common.LINE_BREAK[:1]
            )
        if element.pinfos:
            for pinfo in element.pinfos:
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + "struct"
                    + Common.SPACE_INDENTATION[:1]
                    + element.module_impl_name
                    + "_pinfo_struct * "
                    + pinfo.name
                    + ";"
                    + Common.LINE_BREAK[:1]
                )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        return generation

    def _generate_platform_hook_struct(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "struct"
            + Common.SPACE_INDENTATION[:1]
            + element.module_impl_name
            + Common.switch_lang("__", "::Container::", element.language)
            + "platform_hook"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_hook = {"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_inst_name.upper()
            + "_"
            + component_name.upper()
            + "_ID"
            + ("," if element.properties or element.pinfos else "")
            + Common.SPACE_INDENTATION[:1]
            + "/* mod_id */"
            + Common.LINE_BREAK[:1]
        )
        if element.properties:
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "&"
                + element.module_inst_name
                + "_"
                + component_name
                + "_properties"
                + ("," if element.pinfos else "")
                + Common.SPACE_INDENTATION[:1]
                + "/* properties */"
                + Common.LINE_BREAK[:1]
            )
        if element.pinfos:
            for i, pinfo in enumerate(element.pinfos):
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + "&"
                    + element.module_inst_name
                    + "_"
                    + component_name
                    + "_pinfo_struct_"
                    + pinfo.name
                    + ("," if i + 1 != len(element.pinfos) else "")
                    + Common.LINE_BREAK[:1]
                )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "};" + Common.LINE_BREAK[:2]
        return generation

    def _generate_container(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + "::Container"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_container"
            + Common.SPACE_INDENTATION[:1]
            + "(&"
            + element.module_inst_name
            + "_"
            + component_name
            + "_hook);"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_user_context(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + Common.switch_lang("_", "::", element.language)
            + "user_context"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_user_context;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_warm_start_context(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + Common.switch_lang("_", "::", element.language)
            + "warm_start_context"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_warm_start_context;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_context_struct(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + "__context"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_Context;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_module(self, element: PlatformHook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + element.module_impl_name
            + "::Module"
            + Common.SPACE_INDENTATION[:1]
            + element.module_inst_name
            + "_"
            + component_name
            + "_Module;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def generate(self, element: PlatformHook, types_helper):
        """"""
        self.property_value_helper = PropertyValueHelper(element.language)
        generation = ""
        key = element.component_impl_name + ":" + element.module_impl_name
        if key not in self.visited:
            self.visited.append(key)
            if element.properties:
                generation += self._generate_properties_struct_init(element)
            if element.pinfos:
                generation += self._generate_pinfo_struct_init(element)
            generation += self._generate_platform_hook_struct_init(element)
        if element.language == "c++" and element.pinfos:
            generation += self._generate_pinfo_files(element)
        for component_name in element.component_names:
            if element.properties:
                generation += self._generate_properties_struct(element, component_name, types_helper)
            if element.pinfos:
                generation += self._generate_pinfo_struct(element, component_name)
            generation += self._generate_platform_hook_struct(element, component_name)
            if element.language == "c++":
                generation += self._generate_container(element, component_name)
                if element.has_user_context:
                    generation += self._generate_user_context(element, component_name)
                if element.has_warm_start_context:
                    generation += self._generate_warm_start_context(element, component_name)
            generation += Common.switch_lang(
                self._generate_context_struct(element, component_name),
                self._generate_module(element, component_name),
                element.language,
            )
        return generation
