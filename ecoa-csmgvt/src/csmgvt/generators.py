# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Generation classes.
"""

# Standard library imports
import logging
import os

# Local imports
from csmgvt.component.external import ExternalInterfaceGenerator
from csmgvt.component.module.cmakelists import CMakeListsGenerator as ModuleCMakeListsGenerator
from csmgvt.csm.cmakelists import CMakeListsGenerator as CSMCMakeListsGenerator
from csmgvt.csm.container import ContainerMockGenerator
from csmgvt.csm.main import MainGenerator

logger = logging.getLogger(__name__)


def generate_directory(path: str) -> None:
    """Generates the path leading to a directory.

    Arg:
        path (str) : The directory path.
    """
    logger.debug("Attempt to create directory %s", path)
    if os.path.exists(path):
        logger.debug("%s directory already exists !", path)
    else:
        os.mkdir(path)
        logger.debug("Created directory %s", path)


class ComponentsGenerator:
    """The Components Generator."""

    def __init__(self, ecoa_model, output: str, force: bool):
        self._ecoa_model = ecoa_model
        self._output = output
        self._force = force

    def generate(self) -> None:
        """Generates the following files for all modules of all components:
        - <output>/#component_impl_name#/#component_impl_name#_External_Interface.h(pp)
        - <output>/#component_impl_name#/#module_impl_name#/CMakeLists.txt
        """
        for path, component_impl in self._ecoa_model.components.items():
            component_impl_name = os.path.normpath(path).split(os.path.sep)[-2]
            component_directory_path = os.path.join(self._output, component_impl_name)
            generate_directory(component_directory_path)
            ExternalInterfaceGenerator(
                self._ecoa_model, component_directory_path, component_impl_name, self._force
            ).generate()
            for module_impl in component_impl.module_implementation:
                module_directory_path = os.path.join(component_directory_path, module_impl.name)
                generate_directory(module_directory_path)
                ModuleCMakeListsGenerator(
                    self._ecoa_model,
                    module_directory_path,
                    component_impl_name,
                    module_impl.name,
                    module_impl.language.lower(),
                    self._force,
                ).generate()


class CSMGenerator:
    """The CSM Generator.

    Args:
        ecoa_model : The ECOA model.
        output (str) : The output directory path.
        force (bool) : True if the files can be overwritten, false otherwise.
    """

    def __init__(self, ecoa_model, output: str, force: bool):
        self._ecoa_model = ecoa_model
        self._output = output
        self._force = force

    def generate(self) -> None:
        """Generates the following files:
        - <output>/src/main.cpp.
        - <output>/src/CSM_#project_name#.cpp.
        - <output>/CMakeLists.txt.
        """
        generate_directory(os.path.join(self._output, "src"))
        MainGenerator.generate(self._ecoa_model, self._output, self._force)
        ContainerMockGenerator.generate(self._ecoa_model, self._output, self._force)
        CSMCMakeListsGenerator(self._ecoa_model, self._output, self._force).generate()
