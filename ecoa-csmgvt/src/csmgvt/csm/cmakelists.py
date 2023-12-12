# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""CSM CMakeLists generation class.
"""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.cmakelists import CMakeListsGenerator as CommonCMakeListsGenerator
from ecoa_toolset.generators.common import Common

logger = logging.getLogger(__name__)


class CMakeListsGenerator(CommonCMakeListsGenerator):
    """The CSM CMakeLists Generator.

    Args:
        ecoa_model : The ECOA model.
        path (str) : The generation path.
        force (bool): True if the file can be overwritten, False otherwise.
    """

    def __init__(self, ecoa_model, path: str, force: bool):
        super().__init__(path)
        self._ecoa_model = ecoa_model
        self._force = force
        self._components = {
            os.path.normpath(path).split(os.path.sep)[-2]: [
                module_impl.name for module_impl in component_impl.module_implementation
            ]
            for path, component_impl in self._ecoa_model.components.items()
        }

    def _generate_header(self) -> str:
        # CMakeLists.txt header comment
        generation = (
            "#"
            + Common.LINE_BREAK[:1]
            + "# CMakeLists.txt for the CSM of "
            + self._ecoa_model.project_name
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
        generation += "# Setting the project name" + Common.LINE_BREAK[:2] + "project(csm)" + Common.LINE_BREAK[:2]
        # set the language standard
        generation += (
            "# Setting the C++ standard to C++14"
            + Common.LINE_BREAK[:2]
            + "set(CMAKE_CXX_STANDARD 14)"
            + Common.LINE_BREAK[:2]
        )
        # set the ECOA project directory path
        relative_path = "/".join(
            os.path.normpath(
                os.path.split(Common.compute_relative_path(self._path, self._ecoa_model.project_path))[0]
            ).split(os.path.sep)
        )
        generation += (
            "# Setting the ECOA project directory path"
            + Common.LINE_BREAK[:2]
            + "set(ECOA_PROJECT_DIRECTORY ${PROJECT_SOURCE_DIR}"
            + ("/" if relative_path else "")
            + relative_path
            + ")"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_headers_directories(self, container: bool = False) -> str:
        generation = Common.LINE_BREAK[:1]
        if container:
            for component_impl_name in self._components.keys():
                generation += Common.SPACE_INDENTATION[:2] + component_impl_name + Common.LINE_BREAK[:1]
        generation += Common.SPACE_INDENTATION[:2] + "0-Types/inc" + Common.LINE_BREAK[:1]
        for component_impl, module_impls in self._components.items():
            for module_impl in module_impls:
                for header in ["inc", "inc-gen"]:
                    generation += (
                        Common.SPACE_INDENTATION[:2]
                        + "${ECOA_PROJECT_DIRECTORY}/4-ComponentImplementations/"
                        + component_impl
                        + "/"
                        + module_impl
                        + "/"
                        + header
                        + Common.LINE_BREAK[:1]
                    )
        generation += ")" + Common.LINE_BREAK[:2]
        return generation

    def _generate_listing(self) -> str:
        # Listing for the csm executable
        generation = (
            "# Listing the source files and headers directories for the csm executable"
            + Common.LINE_BREAK[:2]
            + "set(CSM_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "src/main.cpp"
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(CSM_HEADERS_DIRECTORIES"
            + self._generate_headers_directories()
        )
        # Listing for the container library
        generation += (
            "# Listing the source files and headers directories for the container library"
            + Common.LINE_BREAK[:2]
            + "set(CONTAINER_SOURCES"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "src/CSM_"
            + self._ecoa_model.project_name
            + ".cpp"
            + Common.LINE_BREAK[:1]
            + ")"
            + Common.LINE_BREAK[:2]
            + "set(CONTAINER_HEADERS_DIRECTORIES"
            + self._generate_headers_directories(container=True)
        )
        return generation

    def _generate_add_executable_and_library(self) -> str:
        generation = (
            "# Creating the csm executable"
            + Common.LINE_BREAK[:2]
            + "add_executable(${PROJECT_NAME} ${CSM_SOURCES})"
            + Common.LINE_BREAK[:2]
            + "# Creating the container library"
            + Common.LINE_BREAK[:1]
            + "# In Linux, by default, the container library should be compiled as a shared library"
            + Common.LINE_BREAK[:1]
            + "# In Windows or when profiling in Linux, the container library should be compiled as a static library"
            + Common.LINE_BREAK[:2]
            + 'if((UNIX AND BUILD_TYPE_UPPER STREQUAL "PROFILING") OR WIN32)'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(container STATIC ${CONTAINER_SOURCES})"
            + Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "add_library(container SHARED ${CONTAINER_SOURCES})"
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
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_add_subdirectories(self) -> str:
        generation = "# Calling subdirectories" + Common.LINE_BREAK[:2]
        for component_impl_name, module_impl_names in self._components.items():
            for module_impl_name in module_impl_names:
                generation += "add_subdirectory(" + component_impl_name + "/" + module_impl_name + ")"
                generation += Common.LINE_BREAK[:1]
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_target_include_directories(self) -> str:
        generation = (
            "# Providing the include directories"
            + Common.LINE_BREAK[:2]
            + "target_include_directories(${PROJECT_NAME} PRIVATE ${CSM_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:1]
            + "target_include_directories(container PRIVATE ${CONTAINER_HEADERS_DIRECTORIES})"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_target_link_libraries(self) -> str:
        generation = (
            "# Linking the csm executable and the container library with profiling and coverage libraries if needed"
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
            + "endif()"
            + Common.LINE_BREAK[:2]
            + "# Linking the csm executable with the libraries"
            + Common.LINE_BREAK[:2]
            + "target_link_libraries(${PROJECT_NAME} PRIVATE"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "container"
            + Common.LINE_BREAK[:1]
        )
        for module_impl_names in self._components.values():
            for module_impl_name in module_impl_names:
                generation += Common.SPACE_INDENTATION[:2] + module_impl_name + Common.LINE_BREAK[:1]
        generation += ")" + Common.LINE_BREAK[:1]
        return generation

    def generate(self):
        """Generates the following file:
        - <output>/CMakeLists.txt.
        """
        file_name = "CMakeLists.txt"
        file_path = os.path.join(self._path, file_name)
        if os.path.exists(file_path) and self._force:
            logger.debug("%s already exists, forcing, overwriting it...", file_path)
        with open(file_path, "w") as f:
            f.write(self._generate_header())
            f.write(self._generate_configuration_types(shared=False))
            f.write(self._generate_listing())
            f.write(self._generate_add_executable_and_library())
            f.write(self._generate_compiler_options())
            f.write(self._generate_add_subdirectories())
            f.write(self._generate_target_include_directories())
            f.write(self._generate_target_link_libraries())
        logger.debug("CMakeLists.txt for the CSM of %s generated", self._ecoa_model.project_name)
