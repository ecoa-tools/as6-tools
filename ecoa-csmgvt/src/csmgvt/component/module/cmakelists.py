# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module CMakeLists generation class.
"""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.cmakelists import CMakeListsGenerator as CommonCMakeListsGenerator
from ecoa_toolset.generators.common import Common

logger = logging.getLogger(__name__)


class CMakeListsGenerator(CommonCMakeListsGenerator):
    """The Module CMakeLists Generator.

    Args:
        ecoa_model : The ECOA model.
        path (str) : The generation path.
        component_impl_name (str) : The component implementation name.
        module_impl_name (str) : The module implementation name.
        language (str) : The module implementation language.
        force (bool) : True if the file can be overwritten, False otherwise.
    """

    def __init__(
        self, ecoa_model, path: str, component_impl_name: str, module_impl_name: str, language: str, force: bool
    ):
        super().__init__(path)
        self._ecoa_model = ecoa_model
        self._component_impl_name = component_impl_name
        self._module_impl_name = module_impl_name
        self._language = language
        self._force = force

    def _generate_header(self) -> str:
        # CMakeLists.txt header comment
        generation = (
            "#"
            + Common.LINE_BREAK[:1]
            + "# CMakeLists.txt for"
            + Common.SPACE_INDENTATION[:1]
            + self._module_impl_name
            + Common.LINE_BREAK[:1]
            + "#"
            + Common.LINE_BREAK[:2]
        )
        # cmake_minimum_required
        generation += (
            "# Setting minimum required version to access CMake modern features"
            + Common.LINE_BREAK[:2]
            + "cmake_minimum_required(VERSION 3.0)"
            + Common.LINE_BREAK[:2]
        )
        # set CMAKE_STANDARD
        generation += (
            "# Setting the C"
            + Common.switch_lang("", "++", self._language)
            + " standard to C"
            + Common.switch_lang("11", "++14", self._language)
            + Common.LINE_BREAK[:2]
            + "set(CMAKE_C"
            + Common.switch_lang("", "XX", self._language)
            + "_STANDARD "
            + Common.switch_lang("11", "14", self._language)
            + ")"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_listing(self) -> str:
        generation = (
            "# Listing the source files and headers directories for module library"
            + Common.LINE_BREAK[:2]
            + "set(MODULE_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/"
            + self._component_impl_name
            + "/"
            + self._module_impl_name
            + "/src/"
            + self._module_impl_name
            + ".c"
            + Common.switch_lang("", "pp", self._language)
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(MODULE_HEADERS_DIRECTORIES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + ".."
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "../../0-Types/inc"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/"
            + self._component_impl_name
            + "/"
            + self._module_impl_name
            + "/inc"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/"
            + self._component_impl_name
            + "/"
            + self._module_impl_name
            + "/inc-gen"
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_add_library(self) -> str:
        generation = (
            "# Creating the module library"
            + Common.LINE_BREAK[:1]
            + "# In Linux, by default, the "
            + self._module_impl_name
            + " library should be compiled as a shared library"
            + Common.LINE_BREAK[:1]
            + "# In Windows or when profiling in Linux, the "
            + self._module_impl_name
            + " library should be compiled as a static library"
            + Common.LINE_BREAK[:2]
            + 'if((UNIX AND BUILD_TYPE_UPPER STREQUAL "PROFILING") OR WIN32)'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library("
            + self._module_impl_name
            + " STATIC ${MODULE_SOURCES})"
            + Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library("
            + self._module_impl_name
            + " SHARED ${MODULE_SOURCES})"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_include_local_cmake(self) -> str:
        generation = (
            "# Include module local.cmake if it exists"
            + Common.LINE_BREAK[:2]
            + 'if(EXISTS "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/'
            + self._component_impl_name
            + "/"
            + self._module_impl_name
            + '/local.cmake")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'include("${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/'
            + self._component_impl_name
            + "/"
            + self._module_impl_name
            + '/local.cmake")'
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
            + "# Include component local.cmake if it exists"
            + Common.LINE_BREAK[:2]
            + 'if(EXISTS "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/'
            + self._component_impl_name
            + '/local.cmake")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'include("${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/'
            + self._component_impl_name
            + '/local.cmake")'
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_compiler_options(self) -> str:
        generation = (
            "# Custom CMake flags"
            + Common.LINE_BREAK[:2]
            + "if(64BIT_SUPPORT)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_definitions("
            + self._module_impl_name
            + " PRIVATE ECOA_64BIT_SUPPORT)"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        # Compiler options depending on the OS and generator and for the custom build types
        generation += (
            "# Extra flags to comply with the language standards and configuration types"
            + Common.LINE_BREAK[:2]
            + "if(WIN32)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options("
            + self._module_impl_name
            + " PRIVATE -Wall)"
            + Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + self._module_impl_name
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "PRIVATE -W"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "-Wall"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "-Wextra"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "-ansi"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "-pedantic"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "$<$<CONFIG:Profiling>:-pg>"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:12]
            + "$<$<CONFIG:Coverage>:-O0;--coverage>)"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_target_include_directories(self) -> str:
        generation = (
            "# Providing the include directories"
            + Common.LINE_BREAK[:2]
            + "target_include_directories("
            + self._module_impl_name
            + " PRIVATE ${MODULE_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_target_link_libraries(self) -> str:
        generation = (
            "# Linking the module library with profiling and coverage libraries if needed"
            + Common.LINE_BREAK[:2]
            + "if(UNIX)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_link_libraries("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + self._module_impl_name
            + " PRIVATE $<$<CONFIG:Profiling>:-pg> $<$<CONFIG:Coverage>:--coverage>)"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
            + "# Linking the module library with the container library"
            + Common.LINE_BREAK[:2]
            + "target_link_libraries("
            + self._module_impl_name
            + " PRIVATE container)"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def generate(self) -> None:
        """Generates the following file:
        - <output>/#component_impl_name#/#module_impl_name#/CMakeLists.txt.
        """
        file_name = "CMakeLists.txt"
        file_path = os.path.join(self._path, file_name)
        if os.path.exists(file_path) and self._force:
            logger.debug("%s already exists, forcing, overwriting it...", file_path)
        with open(file_path, "w") as f:
            f.write(self._generate_header())
            f.write(self._generate_listing())
            f.write(self._generate_add_library())
            f.write(self._generate_include_local_cmake())
            f.write(self._generate_compiler_options())
            f.write(self._generate_target_include_directories())
            f.write(self._generate_target_link_libraries())
        logger.debug("CMakeLists.txt for %s generated", self._module_impl_name)
