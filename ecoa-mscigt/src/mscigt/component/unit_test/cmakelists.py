# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Unit Test CMakeLists generation class.
"""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.cmakelists import CMakeListsGenerator as CommonCMakeListsGenerator
from ecoa_toolset.generators.common import Common

logger = logging.getLogger(__name__)


class UnitTestCMakeListsGenerator(CommonCMakeListsGenerator):
    """The Unit Test CMakeLists Generator.

    Args:
        path (str) : The generation path.
        module_impl_name (str) : The module implementation name.
        language (str) : The module implementation language.
    """

    def __init__(self, path: str, module_impl_name: str, language: str, output_path: str):
        super().__init__(path)
        self._module_impl_name = module_impl_name
        self._language = language
        self._output_path = output_path

    def _generate_header(self) -> str:
        # CMakeLists.txt header comment
        generation = (
            "#"
            + Common.LINE_BREAK[:1]
            + "# CMakeLists.txt for unit_test_"
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
        # set PROJECT_NAME
        generation += (
            "# Setting the project name"
            + Common.LINE_BREAK[:2]
            + "project(unit_test_"
            + self._module_impl_name
            + ")"
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
        # set CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS
        generation += (
            "# Setting the WINDOWS_EXPORT_ALL_SYMBOLS property"
            + Common.LINE_BREAK[:2]
            + "set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)"
            + Common.LINE_BREAK[:2]
        )
        # set the output directory path
        relative_path = "/".join(
            os.path.normpath(Common.compute_relative_path(self._path, self._output_path)).split(os.path.sep)
        )
        generation += (
            "# Setting the output directory path"
            + Common.LINE_BREAK[:2]
            + "set(OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}"
            + ("/" if relative_path else "")
            + relative_path
            + ")"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_headers_directories(self) -> str:
        generation = (
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${OUTPUT_DIRECTORY}/0-Types/inc"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${PROJECT_SOURCE_DIR}/../inc"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${PROJECT_SOURCE_DIR}/../inc-gen"
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_listing(self) -> str:
        # Listing for the unit test executable
        generation = (
            "# Listing the source files and headers directories for the unit test executable"
            + Common.LINE_BREAK[:2]
            + "set(UNIT_TEST_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "main.c"
            + Common.switch_lang("", "pp", self._language)
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(UNIT_TEST_HEADERS_DIRECTORIES"
            + self._generate_headers_directories()
        )
        # Listing for the container library
        generation += (
            "# Listing the source files and headers directories for the container library"
            + Common.LINE_BREAK[:2]
            + "set(CONTAINER_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + self._module_impl_name
            + "_container_mock.c"
            + Common.switch_lang("", "pp", self._language)
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(CONTAINER_HEADERS_DIRECTORIES"
            + self._generate_headers_directories()
        )
        # Listing for the module library
        generation += (
            "# Listing the source files and headers directories for the module library"
            + Common.LINE_BREAK[:2]
            + "set(MODULE_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "${PROJECT_SOURCE_DIR}/../src/"
            + self._module_impl_name
            + ".c"
            + Common.switch_lang("", "pp", self._language)
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(MODULE_HEADERS_DIRECTORIES"
            + self._generate_headers_directories()
        )
        return generation

    def _generate_include_local_cmake(self) -> str:
        generation = (
            "# Include module local.cmake if it exists"
            + Common.LINE_BREAK[:2]
            + 'if(EXISTS "${PROJECT_SOURCE_DIR}/../local.cmake")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'include("${PROJECT_SOURCE_DIR}/../local.cmake")'
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
            + "# Include component local.cmake if it exists"
            + Common.LINE_BREAK[:2]
            + 'if(EXISTS "${PROJECT_SOURCE_DIR}/../../local.cmake")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'include("${PROJECT_SOURCE_DIR}/../../local.cmake")'
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_add_executable_and_libraries(self) -> str:
        generation = (
            "# Creating the unit test executable"
            + Common.LINE_BREAK[:2]
            + "add_executable(${PROJECT_NAME} ${UNIT_TEST_SOURCES})"
            + Common.LINE_BREAK[:2]
            + "# Creating the container and module libraries"
            + Common.LINE_BREAK[:1]
            + "# By default, these librairies should be compiled as shared libraries"
            + Common.LINE_BREAK[:1]
            + "# When profiling in Linux, these librairies should be compiled as static libraries"
            + Common.LINE_BREAK[:2]
            + 'if(UNIX AND BUILD_TYPE_UPPER STREQUAL "PROFILING")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(container STATIC ${CONTAINER_SOURCES})"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(module STATIC ${MODULE_SOURCES})"
            + Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(container SHARED ${CONTAINER_SOURCES})"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(module SHARED ${MODULE_SOURCES})"
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
            + "target_compile_definitions(${PROJECT_NAME} PRIVATE ECOA_64BIT_SUPPORT)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_definitions(container PRIVATE ECOA_64BIT_SUPPORT)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_definitions(module PRIVATE ECOA_64BIT_SUPPORT)"
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
            + "set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options(${PROJECT_NAME} PRIVATE -Wall)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options(container PRIVATE -Wall)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options(module PRIVATE -Wall)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'if(CMAKE_GENERATOR MATCHES "Visual Studio")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT"
            + Common.SPACE_INDENTATION[:1]
            + "${PROJECT_NAME})"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "endif()"
            + Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "${PROJECT_NAME}"
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
            + "-Wno-uninitialized"
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
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "container"
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
            + Common.SPACE_INDENTATION[:2]
            + "target_compile_options("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "module"
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
            + "target_include_directories(${PROJECT_NAME} PRIVATE ${UNIT_TEST_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:1]
            + "target_include_directories(container PRIVATE ${CONTAINER_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:1]
            + "target_include_directories(module PRIVATE ${MODULE_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_target_link_libraries(self) -> str:
        generation = (
            "# Linking the unit test executable, the container library and the module library "
            + "with profiling and coverage libraries if needed"
            + Common.LINE_BREAK[:2]
            + "if(UNIX)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_link_libraries("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "${PROJECT_NAME} PRIVATE $<$<CONFIG:Coverage>:--coverage>)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_link_libraries("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "container PRIVATE $<$<CONFIG:Profiling>:-pg> $<$<CONFIG:Coverage>:--coverage>)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "target_link_libraries("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "module PRIVATE $<$<CONFIG:Profiling>:-pg> $<$<CONFIG:Coverage>:--coverage>)"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
            + "# Linking the module library with the container library"
            + Common.LINE_BREAK[:2]
            + "target_link_libraries(module PRIVATE container)"
            + Common.LINE_BREAK[:2]
            + "# Linking the unit test executable with the libraries"
            + Common.LINE_BREAK[:2]
            + "target_link_libraries(${PROJECT_NAME} PRIVATE container module)"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def generate(self) -> None:
        """Generates the following file:
        .
        └── 4-ComponentImplementations
            └── #component_impl_name#
                └── #module_impl_name#
                    └── tests
                        └── CMakeLists.txt
        """
        file_name = "CMakeLists.txt"
        file_path = os.path.join(self._path, file_name)
        with open(file_path, "w") as f:
            f.write(self._generate_header())
            f.write(self._generate_configuration_types())
            f.write(self._generate_listing())
            f.write(self._generate_include_local_cmake())
            f.write(self._generate_add_executable_and_libraries())
            f.write(self._generate_compiler_options())
            f.write(self._generate_target_include_directories())
            f.write(self._generate_target_link_libraries())
        logger.debug("CMakeLists.txt for unit_test_%s generated", self._module_impl_name)
