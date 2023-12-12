# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module unit tests container mock source code generation.
"""

# Standard library imports
import logging
import os

# Local imports
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.container.generator import ContainerGenerator
from ecoa_toolset.generators.helpers.global_variable import CMGlobalVariable, CMGlobalVariableHelper
from ecoa_toolset.generators.helpers.platform_hook import PlatformHook, PlatformHookHelper
from ecoa_toolset.visitors.container import ContainerVisitor

logger = logging.getLogger(__name__)


class ContainerMockVisitor(ContainerVisitor):
    """The Container Mock Visitor"""

    _ecoa_model = None

    def __init__(self, generator, ecoa_model):
        super().__init__(generator)
        self._ecoa_model = ecoa_model

    def visit_CMGlobalVariable(self, element: CMGlobalVariable, **kwargs) -> str:
        generation = self._generator.global_variable.generate(element)
        return generation

    def visit_hook(self, element: PlatformHook, **kwargs) -> str:
        generation = self._generator.module_instantiation.generate(element, self._ecoa_model.types_helper)
        return generation


class UnitTestContainerMockGenerator:
    """"""

    _ecoa_model = None
    _path: str = None
    _component_impl_name: str = None
    _module_impl_name: str = None
    _language: str = None
    _templates: Templates = None
    _global_variable_helper = None
    _platform_hook_helper = None
    _generator = None
    _visitor = None

    def __init__(
        self,
        ecoa_model,
        path: str,
        component_impl_name: str,
        module_impl_name: str,
        language: str,
        templates: Templates,
    ) -> None:
        self._ecoa_model = ecoa_model
        self._path = path
        self._component_impl_name = component_impl_name
        self._module_impl_name = module_impl_name
        self._language = language
        self._templates = templates
        self._global_variable_helper = CMGlobalVariableHelper(self._ecoa_model)
        self._platform_hook_helper = PlatformHookHelper(self._ecoa_model)
        self._generator = ContainerGenerator(0, 2, True, True)
        self._visitor = ContainerMockVisitor(self._generator, self._ecoa_model)

    def generate(self) -> None:
        """Generates the containers functions."""
        ext = ".c" + Common.switch_lang("", "pp", self._language)
        module_impl = self._ecoa_model.module_impls.get(self._component_impl_name + ":" + self._module_impl_name)
        module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
        file_name = self._module_impl_name + "_container_mock" + ext
        file_path = os.path.join(self._path, file_name)
        try:
            with open(file_path, "x") as f:
                # Header comment and standards includes
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        "Container Mock Code for Module " + self._module_impl_name,
                    )
                )
                f.write("/* Standards libraries */" + Common.LINE_BREAK[:1])
                libraries = [
                    "stdlib",
                    "time",
                    "stdio",
                    "string",
                ]
                for library in libraries:
                    f.write("#include <" + library + ".h>" + Common.LINE_BREAK[:1])
                if self._language == "c++":
                    f.write("#include <chrono>" + Common.LINE_BREAK[:1])
                    f.write("#include <cstring>" + Common.LINE_BREAK[:1])

                f.write(
                    Common.LINE_BREAK[:1]
                    + "/* ECOA standard types */"
                    + Common.LINE_BREAK[:1]
                    + '#include "ECOA.h'
                    + Common.switch_lang("", "pp", self._language)
                    + '"'
                    + Common.LINE_BREAK[:2]
                )

                # Module, container and container types includes
                f.write("/* Module interfaces */" + Common.LINE_BREAK[:1])
                interfaces_type = ["", "_container", "_container_types"]
                for interface in interfaces_type:
                    f.write(
                        '#include "'
                        + self._module_impl_name
                        + interface
                        + ".h"
                        + Common.switch_lang("", "pp", self._language)
                        + '"'
                        + Common.LINE_BREAK[:1]
                    )

                # Modules ID
                component_names = self._ecoa_model.component_names.items()
                module_inst_names = [
                    module_inst.name
                    for key, module_inst in self._ecoa_model.module_insts.items()
                    if module_inst.implementation_name == self._module_impl_name
                    and key.split(":")[0] == self._component_impl_name
                ]
                f.write(
                    Common.LINE_BREAK[:1]
                    + "/* Modules ID */"
                    + Common.LINE_BREAK[:2]
                    + self._generator.generate_modules_id(component_names, module_inst_names=module_inst_names)
                )

                # Global variables
                global_variables = self._global_variable_helper.find_all(module_impl_name=self._module_impl_name)
                for global_variable_type, variables in global_variables.items():
                    if variables:
                        f.write(
                            "/* Global"
                            + Common.SPACE_INDENTATION[:1]
                            + global_variable_type
                            + Common.SPACE_INDENTATION[:1]
                            + "*/"
                            + Common.LINE_BREAK[:2]
                        )
                        for variable in variables:
                            f.write(variable.accept(self._visitor))
                        f.write(Common.LINE_BREAK[:1])

                # Generate container constructors for modules implemented in c++
                if self._language == "c++":
                    f.write("/* Container constructor */" + Common.LINE_BREAK[:2])
                    f.write(self._generator.generate_container_constructor(self._module_impl_name))

                # Hooks
                f.write("/* Modules instanciation */" + Common.LINE_BREAK[:2])
                hooks = self._platform_hook_helper.find_all(
                    component_impl_name=self._component_impl_name, module_impl_name=self._module_impl_name
                ).values()
                for hook in hooks:
                    f.write(hook.accept(self._visitor))
                f.write(self._generator.generate_cm_initialize(hooks))
                pinfos = self._ecoa_model.pinfos.get(self._component_impl_name + ":" + self._module_impl_name, [])
                if pinfos:
                    f.write(self._generator.generate_cm_shutdown(hooks))

                # Get property value functions
                properties = self._ecoa_model.properties.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if properties:
                    f.write("/* Get property value operations */" + Common.LINE_BREAK[:2])
                    for property in properties:
                        f.write(property.accept(self._visitor))

                # Logs functions
                log = self._ecoa_model.logs.get(self._component_impl_name + ":" + self._module_impl_name)
                if log:
                    f.write("/* Log operations */" + Common.LINE_BREAK[:2])
                    f.write(log.accept(self._visitor))

                # Time services functions
                time = self._ecoa_model.times.get(self._component_impl_name + ":" + self._module_impl_name)
                if time:
                    f.write("/* Time operations */" + Common.LINE_BREAK[:2])
                    f.write(time.accept(self._visitor))
                    f.write(time.accept(self._visitor, resolution=True))

                # Read and write versioned data container functions
                data_read = self._ecoa_model.data_read.get(self._component_impl_name + ":" + self._module_impl_name, [])
                data_written = self._ecoa_model.data_written.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if data_read or data_written:
                    f.write("/* Versioned data container operations */" + Common.LINE_BREAK[:2])
                    for read in data_read:
                        f.write(read.accept(self._visitor))
                    for write in data_written:
                        f.write(write.accept(self._visitor))

                # Event send functions
                events_send = self._ecoa_model.events_send.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if events_send:
                    f.write("/* Event send operations */" + Common.LINE_BREAK[:2])
                    for send in events_send:
                        f.write(send.accept(self._visitor))

                # Request and response functions
                requests_send = self._ecoa_model.requests_send.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                requests_received = self._ecoa_model.requests_received.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if requests_send or requests_received:
                    f.write("/* Request response operations */" + Common.LINE_BREAK[:2])
                    for send in requests_send:
                        f.write(send.accept(self._visitor))
                    for received in requests_received:
                        f.write(received.accept(self._visitor))

                # Recovery action functions
                if module_type.is_fault_handler:
                    f.write("/* Recovery action operations */" + Common.LINE_BREAK[:2])
                    f.write(self._generator.recovery_action.generate((module_impl.name, module_impl.language.lower())))

                # Save Warm Start Context functions
                if module_type.has_warm_start_context:
                    f.write("/* Save Warm Start Context operations */" + Common.LINE_BREAK[:2])
                    f.write(
                        self._generator.save_warm_start_context.generate(
                            (module_impl.name, module_impl.language.lower())
                        )
                    )

                # PInfo
                if pinfos:
                    f.write("/* Pinfo operations */" + Common.LINE_BREAK[:2])
                    for pinfo in pinfos:
                        f.write(pinfo.accept(self._visitor))

            logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
