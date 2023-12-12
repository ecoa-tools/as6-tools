# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Container Interfaces and Module Skeletons generator."""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.common import Common

# Local imports
from mscigt.component.container.interface import ContainerInterfaceGenerator
from mscigt.component.container.types import ContainerTypesGenerator
from mscigt.component.module.interface import ModuleInterfaceGenerator
from mscigt.component.module.source import ModuleSourceGenerator
from mscigt.component.module.user import ModuleUserGenerator
from mscigt.component.unit_test.cmakelists import UnitTestCMakeListsGenerator
from mscigt.component.unit_test.container_mock import UnitTestContainerMockGenerator
from mscigt.component.unit_test.main import UnitTestMainGenerator
from mscigt.templates import Templates

logger = logging.getLogger(__name__)


class ComponentGenerator:
    """The Component Generator.

    Args:
        ecoa_model : The ECOA model.
        path (str) : The generation directory path.
        component_impl_name (str) : The component implementation name.
        module_impl_name (str) : The module implementation name.
        force (bool) : True if the files can be overwritten, false otherwise.
        templates (Templates): The Templates.
        output_path (str) : The output directory path.
    """

    def __init__(
        self,
        ecoa_model,
        path: str,
        component_impl_name: str,
        module_impl_name: str,
        force: bool,
        templates: Templates,
        output_path: str,
    ) -> None:
        self._ecoa_model = ecoa_model
        self._path = path
        self._component_impl_name = component_impl_name
        self._module_impl_name = module_impl_name
        self._force = force
        self._templates = templates
        self._output_path = output_path
        self._language = self._ecoa_model.module_impls.get(
            self._component_impl_name + ":" + self._module_impl_name
        ).language.lower()

    def generate(self) -> None:
        """Generates the following files:
        .
        └── 4-ComponentImplementations
            └── #component_impl_name#
                └── #module_impl_name#
                    ├── inc
                    │   └── MOD_A_user_context.h(pp)
                    ├── inc-gen
                    │   ├── MOD_A_container_types.h(pp)
                    │   ├── MOD_A_container.h(pp)
                    │   └── MOD_A.h(pp)
                    ├── src
                    │   └── MOD_A.c(pp)
                    └── tests
                        ├── CMakeLists.txt
                        ├── main.c(pp)
                        └── MOD_A_container_mock.c(pp)
        """
        # Create modules and containers files
        inc_directory_path = os.path.join(self._path, "inc")
        Common.create_sub_directory(inc_directory_path, self._force, ignored=True)
        inc_gen_directory_path = os.path.join(self._path, "inc-gen")
        Common.create_sub_directory(inc_gen_directory_path, self._force)
        src_directory_path = os.path.join(self._path, "src")
        Common.create_sub_directory(src_directory_path, self._force, ignored=True)
        tests_directory_path = os.path.join(self._path, "tests")
        Common.create_sub_directory(tests_directory_path, self._force)

        # inc
        ModuleUserGenerator(self._path, self._module_impl_name, self._language, self._templates).generate()
        # inc-gen
        ContainerTypesGenerator(
            self._ecoa_model,
            self._path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        ContainerInterfaceGenerator(
            self._ecoa_model,
            self._path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        ModuleInterfaceGenerator(
            self._ecoa_model,
            self._path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        # src
        ModuleSourceGenerator(
            self._ecoa_model,
            self._path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        # unit-test
        UnitTestContainerMockGenerator(
            self._ecoa_model,
            tests_directory_path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        UnitTestMainGenerator(
            self._ecoa_model,
            self._path,
            self._component_impl_name,
            self._module_impl_name,
            self._language,
            self._templates,
        ).generate()
        UnitTestCMakeListsGenerator(
            tests_directory_path, self._module_impl_name, self._language, self._output_path
        ).generate()
