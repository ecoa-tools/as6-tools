# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Container functions generation class.
"""

# Standard library imports
import os
from typing import Dict, List

# Internal library imports
from ecoa_toolset.generators.container.common import Common
from ecoa_toolset.generators.container.functions.event_send import EventSendGenerator
from ecoa_toolset.generators.container.functions.external import ExternalGenerator
from ecoa_toolset.generators.container.functions.get_value import GetValueGenerator
from ecoa_toolset.generators.container.functions.logs import LogsGenerator
from ecoa_toolset.generators.container.functions.pinfo import PinfoGenerator
from ecoa_toolset.generators.container.functions.recovery_action import RecoveryActionGenerator
from ecoa_toolset.generators.container.functions.request_send import RequestSendGenerator
from ecoa_toolset.generators.container.functions.response_send import ResponseSendGenerator
from ecoa_toolset.generators.container.functions.save_warm_start_context import SaveWarmStartContextGenerator
from ecoa_toolset.generators.container.functions.time import TimeServicesGenerator
from ecoa_toolset.generators.container.functions.versioned_data import VersionedDataGenerator
from ecoa_toolset.generators.container.variables.global_variable import CMGlobalVariableGenerator
from ecoa_toolset.generators.container.variables.module_instantiation import ModuleInstantiationGenerator


class ContainerGenerator:
    """The Container Generator."""

    indent_level: int = None
    indent_step: int = None
    event_send: EventSendGenerator = None
    external: ExternalGenerator = None
    get_value: GetValueGenerator = None
    logs: LogsGenerator = None
    pinfo: PinfoGenerator = None
    recovery_action: RecoveryActionGenerator = None
    request_send: RequestSendGenerator = None
    response_send: ResponseSendGenerator = None
    save_warm_start_context: SaveWarmStartContextGenerator = None
    time: TimeServicesGenerator = None
    versioned_data: VersionedDataGenerator = None
    global_variable: CMGlobalVariableGenerator = None
    module_instantiation: ModuleInstantiationGenerator = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, unit_test: bool):
        self.indent_level = indent_level
        self.indent_step = indent_step
        self.event_send = EventSendGenerator(indent_level, indent_step, body, unit_test)
        self.external = ExternalGenerator(indent_level, indent_step, body)
        self.get_value = GetValueGenerator(indent_level, indent_step, body)
        self.logs = LogsGenerator(indent_level, indent_step, body)
        self.pinfo = PinfoGenerator(indent_level, indent_step, body)
        self.recovery_action = RecoveryActionGenerator(indent_level, indent_step, body)
        self.request_send = RequestSendGenerator(indent_level, indent_step, body, unit_test)
        self.response_send = ResponseSendGenerator(indent_level, indent_step, body, unit_test)
        self.save_warm_start_context = SaveWarmStartContextGenerator(indent_level, indent_step, body)
        self.time = TimeServicesGenerator(indent_level, indent_step, body)
        self.versioned_data = VersionedDataGenerator(indent_level, indent_step, body, unit_test)
        self.global_variable = CMGlobalVariableGenerator()
        self.module_instantiation = ModuleInstantiationGenerator(indent_level, indent_step)

    def generate_container_constructor(self, module_impl_name) -> str:
        generation = (
            module_impl_name
            + "::Container::Container ("
            + module_impl_name
            + "::Container::platform_hook * hook)"
            + Common.LINE_BREAK[:1]
            + "{"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "this->hook = hook;"
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def generate_modules_id(self, component_names: Dict, module_inst_names: List = None) -> str:
        generation = ""
        lines = []
        for key, value in component_names:
            for component_name in value:
                module_inst_name = key.split(":")[-1]
                if module_inst_names is None or module_inst_name in module_inst_names:
                    lines.append("#define " + module_inst_name.upper() + "_" + component_name.upper() + "_ID")
        if lines:
            max_line = len(max(lines, key=len))
        for index, line in enumerate(lines):
            generation += (
                line + Common.SPACE_INDENTATION[: (max_line - len(line) + 1)] + str(index) + Common.LINE_BREAK[:1]
            )
        if lines:
            generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_open_pinfos(self, hook, component_name: str) -> str:
        generation = ""
        for pinfo in hook.pinfos:
            pinfo_file_path = pinfo.values.get(
                hook.component_impl_name + ":" + hook.module_inst_name + ":" + component_name
            )
            generation += (
                Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Context.platform_hook->"
                + pinfo.name
                + '->pinfo_file = fopen("'
                + Common.replace_escape_string(os.path.abspath(pinfo_file_path))
                + '", "rb");'
                + Common.LINE_BREAK[:1]
            )
        return generation

    def _generate_init_context(self, hook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
            + hook.module_inst_name
            + "_"
            + component_name
            + "_Context.platform_hook ="
            + Common.SPACE_INDENTATION[:1]
            + "&"
            + hook.module_inst_name
            + "_"
            + component_name
            + "_hook;"
            + Common.LINE_BREAK[:1]
        )
        if hook.pinfos:
            generation += self._generate_open_pinfos(hook, component_name)
        return generation

    def _generate_init_module(self, hook, component_name: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
            + hook.module_inst_name
            + "_"
            + component_name
            + "_Module.container = &"
            + hook.module_inst_name
            + "_"
            + component_name
            + "_container;"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def generate_cm_initialize(self, hooks: Dict) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void cm_initialize (void)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        for hook in hooks:
            for component_name in hook.component_names:
                tmp = ""
                if hook.language == "c":
                    tmp += self._generate_init_context(hook, component_name)
                elif hook.language == "c++":
                    tmp += self._generate_init_module(hook, component_name)
                if tmp:
                    generation += (
                        Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                        + "/* "
                        + hook.module_inst_name
                        + "_"
                        + component_name
                        + " */"
                        + Common.LINE_BREAK[:1]
                        + tmp
                    )
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        return generation

    def _generate_close_pinfos(self, hook, component_name: str) -> str:
        generation = ""
        for pinfo in hook.pinfos:
            if hook.language == "c":
                generation += (
                    Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                    + "fclose("
                    + hook.module_inst_name
                    + "_"
                    + component_name
                    + "_Context.platform_hook->"
                    + pinfo.name
                    + "->pinfo_file);"
                    + Common.LINE_BREAK[:1]
                )
            elif hook.language == "c++":
                generation += (
                    Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                    + hook.module_inst_name
                    + "_"
                    + component_name
                    + "_hook."
                    + pinfo.name
                    + "->pinfo_file.close();"
                    + Common.LINE_BREAK[:1]
                )
        return generation

    def generate_cm_shutdown(self, hooks: Dict) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void cm_shutdown (void)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        for hook in hooks:
            for component_name in hook.component_names:
                tmp = self._generate_close_pinfos(hook, component_name)
                if tmp:
                    generation += (
                        Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                        + "/* "
                        + hook.module_inst_name
                        + "_"
                        + component_name
                        + " */"
                        + Common.LINE_BREAK[:1]
                        + tmp
                    )
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        return generation
