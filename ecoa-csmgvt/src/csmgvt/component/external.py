# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""External Interface generation class.
"""

# Standard library imports
import logging
import os
from typing import List

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.container.generator import ContainerGenerator
from ecoa_toolset.visitors.container import ContainerVisitor

logger = logging.getLogger(__name__)


class ExternalInterfaceGenerator:
    """The External Interface Generator."""

    _ecoa_model = None
    _path: str = None
    _component_impl_name: str = None
    _force = bool = None

    def __init__(self, ecoa_model, path: str, component_impl_name: str, force: bool):
        self._ecoa_model = ecoa_model
        self._path = path
        self._component_impl_name = component_impl_name
        self._force = force

    def _generate_file_header_comment(self, file_name: str) -> str:
        generation = f"/* @file {file_name}\n"
        generation += f" * External Interface header for Component Implementation {self._component_impl_name}\n"
        generation += " * Generated automatically from specification; do not modify here\n"
        generation += " */\n\n"
        return generation

    def _generate_external_interface(self, externals: List, file_type: str, file_name: str, language: str) -> None:
        indent_level = Common.switch_lang(0, 2, language)
        generator = ContainerGenerator(indent_level, 2, False, False)
        visitor = ContainerVisitor(generator)
        file_path = os.path.join(self._path, file_name)
        if os.path.exists(file_path) and self._force:
            logger.debug("%s already exists, forcing, overwriting it...", file_path)
        with open(file_path, "w") as f:
            f.write(self._generate_file_header_comment(file_name))
            f.write(Common.generate_header_open_guard(self._component_impl_name, language, file_type))
            f.write("/* Standard Types */\n")
            f.write(f'#include <ECOA.h{Common.switch_lang("", "pp", language)}>\n\n')
            f.write("/* Additionally created types */\n")
            f.write(Common.generate_includes(self._ecoa_model.use[self._component_impl_name], language))
            if language == "c++":
                f.write(Common.generate_open_namespace(self._component_impl_name + "_" + file_type))
            for external in externals:
                f.write(external.accept(visitor))
            if language == "c++":
                f.write(Common.generate_close_namespace(self._component_impl_name + "_" + file_type))
            f.write(Common.generate_header_close_guard(self._component_impl_name, language, file_type))
            logger.debug("%s generated", file_path)

    def generate(self) -> None:
        """Generates the following file:
        - <output>/#component_impl_name#/#component_impl_name#_External_Interface.h(pp)
        """
        externals = self._ecoa_model.externals.get(self._component_impl_name, [])
        externals_c = [external for external in externals if external.language == "c"]
        externals_cpp = [external for external in externals if external.language == "c++"]
        file_type = "External_Interface"
        file_name = self._component_impl_name + "_" + file_type + "."
        if externals_c:
            self._generate_external_interface(externals_c, file_type, file_name + "h", "c")
        if externals_cpp:
            self._generate_external_interface(externals_cpp, file_type, file_name + "hpp", "c++")
