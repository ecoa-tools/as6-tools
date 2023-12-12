# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""C++14 Container Mock generation class.
"""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.container.generator import ContainerGenerator
from ecoa_toolset.generators.helpers.global_variable import CMGlobalVariable, CMGlobalVariableHelper
from ecoa_toolset.generators.helpers.platform_hook import PlatformHook, PlatformHookHelper
from ecoa_toolset.models.helpers.module import ModuleHelper
from ecoa_toolset.visitors.container import ContainerVisitor

logger = logging.getLogger(__name__)


class ContainerMockVisitor(ContainerVisitor):
    """The Container Mock Visitor."""

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


class ContainerMockGenerator:
    """The Container Mock Generator."""

    _ecoa_model = None
    _path: str = None
    _global_variable_helper = None
    _module_helper = None
    _platform_hook_helper = None
    _generator = None
    _visitor = None

    @classmethod
    def _generate_recovery_action(cls, module_impl) -> str:
        generation = cls._generator.recovery_action.generate((module_impl.name, module_impl.language.lower()))
        return generation

    @classmethod
    def _generate_save_warm_start_context(cls, module_impl) -> str:
        generation = cls._generator.save_warm_start_context.generate((module_impl.name, module_impl.language.lower()))
        return generation

    @classmethod
    def _generate_container_mock(cls, force: bool) -> None:
        """Generates the container mock source code.

        Args:
            force: True if the file can be overwritten, False otherwise.
        """
        file_name = "CSM_" + cls._ecoa_model.project_name + ".cpp"
        file_path = os.path.join(cls._path, "src", file_name)
        if os.path.exists(file_path) and force:
            logger.debug("%s already exists, forcing, overwriting it...", file_path)
        with open(file_path, "w") as f:
            # Header comment and standards includes
            f.write("/* " + file_name + " */" + Common.LINE_BREAK[:1])
            libraries = [
                "stdlib",
                "time",
                "stdio",
                "string",
                "stdarg",
                "sys/types",
                "sys/stat",
            ]
            for library in libraries:
                f.write("#include <" + library + ".h" + ">" + Common.LINE_BREAK[:1])
            f.write("#include <chrono>" + Common.LINE_BREAK[:1])
            f.write("#include <fstream>" + Common.LINE_BREAK[:1])
            f.write("#include <cstring>" + Common.LINE_BREAK[:1])
            # Component includes
            f.write("/* Components libraries */" + Common.LINE_BREAK[:1])
            for component_impl_name, externals in cls._ecoa_model.externals.items():
                externals_c = [external for external in externals if external.language == "c"]
                externals_cpp = [external for external in externals if external.language == "c++"]
                generation = '#include "' + component_impl_name + "_External_Interface.h"
                if externals_c:
                    f.write(generation + '"' + Common.LINE_BREAK[:1])
                if externals_cpp:
                    f.write(generation + 'pp"' + Common.LINE_BREAK[:1])
            # Module, container and container types includes
            f.write("/* Modules libraries */" + Common.LINE_BREAK[:1])
            for module_impl in cls._ecoa_model.module_impls.values():
                extension = "h" + Common.switch_lang("", "pp", module_impl.language.lower())
                f.write(
                    '#include "'
                    + module_impl.name
                    + "."
                    + extension
                    + '"'
                    + Common.LINE_BREAK[:1]
                    + '#include "'
                    + module_impl.name
                    + "_container."
                    + extension
                    + '"'
                    + Common.LINE_BREAK[:1]
                    + '#include "'
                    + module_impl.name
                    + "_container_types."
                    + extension
                    + '"'
                    + Common.LINE_BREAK[:1]
                )

            # Modules ID
            component_names = cls._ecoa_model.component_names.items()
            f.write(
                Common.LINE_BREAK[:1]
                + "/* Modules ID */"
                + Common.LINE_BREAK[:2]
                + cls._generator.generate_modules_id(component_names)
            )

            # Global variables
            global_variables = cls._global_variable_helper.find_all()
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
                        f.write(variable.accept(cls._visitor))
                    f.write(Common.LINE_BREAK[:1])

            # Generate container constructors for modules implemented in c++
            modules_implemented_in_cpp = cls._module_helper.find_all(language="c++")
            if modules_implemented_in_cpp:
                f.write("/* Container constructors for C++ modules */" + Common.LINE_BREAK[:2])
                for module_impl in modules_implemented_in_cpp.values():
                    f.write(cls._generator.generate_container_constructor(module_impl.name))

            # Hooks
            f.write("/* Modules instanciation */" + Common.LINE_BREAK[:2])
            hooks = cls._platform_hook_helper.find_all().values()
            for hook in hooks:
                f.write(hook.accept(cls._visitor))
            if cls._ecoa_model.module_impls:
                f.write(cls._generator.generate_cm_initialize(hooks))
            if cls._ecoa_model.pinfos:
                f.write(cls._generator.generate_cm_shutdown(hooks))

            # Get property value functions
            properties = cls._ecoa_model.properties
            if properties:
                f.write("/* Get property value operations */" + Common.LINE_BREAK[:2])
                for properties_list in properties.values():
                    for property in properties_list:
                        f.write(property.accept(cls._visitor))

            # Logs functions
            logs = cls._ecoa_model.logs.values()
            if logs:
                f.write("/* Log operations */" + Common.LINE_BREAK[:2])
                for log in logs:
                    f.write(log.accept(cls._visitor))

            # Time functions
            times = cls._ecoa_model.times.values()
            if times:
                f.write("/* Time operations */" + Common.LINE_BREAK[:2])
                for time in times:
                    f.write(time.accept(cls._visitor))
                    f.write(time.accept(cls._visitor, resolution=True))

            # Read and write versioned data container functions
            data_read = [read for v in cls._ecoa_model.data_read.values() for read in v]
            data_written = [written for v in cls._ecoa_model.data_written.values() for written in v]
            if data_read or data_written:
                f.write("/* Versioned data container operations */" + Common.LINE_BREAK[:2])
                for read in data_read:
                    f.write(read.accept(cls._visitor))
                for written in data_written:
                    f.write(written.accept(cls._visitor))

            # Event send functions
            events_send = [send for v in cls._ecoa_model.events_send.values() for send in v]
            if events_send:
                f.write("/* Event send operations */" + Common.LINE_BREAK[:2])
                for send in events_send:
                    f.write(send.accept(cls._visitor))

            # Request response functions (request sync, request async and response send functions)
            requests_send = [send for v in cls._ecoa_model.requests_send.values() for send in v]
            requests_received = [received for v in cls._ecoa_model.requests_received.values() for received in v]
            if requests_send or requests_received:
                f.write("/* Request response operations */" + Common.LINE_BREAK[:2])
                for send in requests_send:
                    f.write(send.accept(cls._visitor))
                for received in requests_received:
                    f.write(received.accept(cls._visitor))

            # Recovery action functions
            modules_with_recovery_action = cls._module_helper.find_all(fault_handler=True)
            if modules_with_recovery_action:
                f.write("/* Recovery action operations */" + Common.LINE_BREAK[:2])
                for module_impl in modules_with_recovery_action.values():
                    f.write(cls._generate_recovery_action(module_impl))

            # Save Warm Start Context functions
            modules_with_warm_start_context = cls._module_helper.find_all(warm_start_context=True)
            if modules_with_warm_start_context:
                f.write("/* Save Warm Start Context operations */" + Common.LINE_BREAK[:2])
                for module_impl in modules_with_warm_start_context.values():
                    f.write(cls._generate_save_warm_start_context(module_impl))

            # PInfo
            pinfos = cls._ecoa_model.pinfos
            if pinfos:
                f.write("/* Pinfo operations */" + Common.LINE_BREAK[:2])
                for pinfos_list in pinfos.values():
                    for pinfo in pinfos_list:
                        f.write(pinfo.accept(cls._visitor))

            # External functions
            externals = [external for v in cls._ecoa_model.externals.values() for external in v]
            if externals:
                f.write("/* Externals operations */" + Common.LINE_BREAK[:2])
                for external in externals:
                    f.write(external.accept(cls._visitor))

            logger.debug("%s generated", file_path)

    @classmethod
    def generate(cls, ecoa_model, path: str, force: bool) -> None:
        """Generates the following file:
            - <output>/src/CSM_#project_name#.cpp.

        Args:
            ecoa_model : The ECOA model.
            path (str) : The generation directory path.
            force (bool) : True if the file can be overwritten, False otherwise.
        """
        cls._path = path
        cls._ecoa_model = ecoa_model
        cls._global_variable_helper = CMGlobalVariableHelper(cls._ecoa_model)
        cls._platform_hook_helper = PlatformHookHelper(cls._ecoa_model)
        cls._module_helper = ModuleHelper(cls._ecoa_model)
        cls._generator = ContainerGenerator(0, 2, True, False)
        cls._visitor = ContainerMockVisitor(cls._generator, cls._ecoa_model)
        cls._generate_container_mock(force)
