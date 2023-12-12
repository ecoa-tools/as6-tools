# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""CMakeLists generation class.
"""

# Internal library imports
from ecoa_toolset.generators.common import Common


class CMakeListsGenerator:
    """The CMakeLists Generator.

    Args:
        path (str) : The generation path.
    """

    def __init__(self, path: str):
        self._path = path

    def _generate_configuration_types(self, shared: bool = True) -> str:
        generation = (
            "# For Windows : setting configuration types; For Linux : setting default build"
            + Common.LINE_BREAK[:1]
            + "# type to Debug and verifing that the build type given by the user is correct"
            + Common.LINE_BREAK[:2]
            + "if(WIN32)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "# Setting configuration types"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "set(CMAKE_CONFIGURATION_TYPES Release Debug Profiling Coverage)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'message(STATUS "[${PROJECT_NAME}] Build types : ${CMAKE_CONFIGURATION_TYPES}")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'set(CMAKE_EXE_LINKER_FLAGS_PROFILING "/PROFILE")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'set(CMAKE_EXE_LINKER_FLAGS_COVERAGE "/DEBUG")'
        )
        if shared:
            generation += (
                Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[:2]
                + 'set(CMAKE_SHARED_LINKER_FLAGS_PROFILING "/PROFILE")'
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[:2]
                + 'set(CMAKE_SHARED_LINKER_FLAGS_COVERAGE "/DEBUG")'
            )
        generation += (
            Common.LINE_BREAK[:1]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "# Setting default build type"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'set(BUILD_TYPE_DEFAULT "Debug")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "if(NOT CMAKE_BUILD_TYPE)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "message("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:6]
            + "STATUS"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:8]
            + '"[${PROJECT_NAME}] Setting build type to ${BUILD_TYPE_DEFAULT} as none was specified"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + ")"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "set(CMAKE_BUILD_TYPE"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:8]
            + "${BUILD_TYPE_DEFAULT}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:8]
            + 'CACHE STRING "" FORCE)'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "endif()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "# Checking the given build type"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "string(TOUPPER ${CMAKE_BUILD_TYPE} BUILD_TYPE_UPPER)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + 'if(BUILD_TYPE_UPPER STREQUAL "RELEASE"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:5]
            + 'OR BUILD_TYPE_UPPER STREQUAL "DEBUG"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:5]
            + 'OR BUILD_TYPE_UPPER STREQUAL "PROFILING"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:5]
            + 'OR BUILD_TYPE_UPPER STREQUAL "COVERAGE")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + 'message(STATUS "[${PROJECT_NAME}] Build type : ${CMAKE_BUILD_TYPE}")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + 'if(BUILD_TYPE_UPPER STREQUAL "MINSIZEREL"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:7]
            + 'OR BUILD_TYPE_UPPER STREQUAL "RELWITHDEBINFO")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:6]
            + "message("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:8]
            + "FATAL_ERROR"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:10]
            + '"[${PROJECT_NAME}] Error : build type ${CMAKE_BUILD_TYPE} not supported for this project"'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:6]
            + ")"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "else()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:6]
            + "message("
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:8]
            + "FATAL_ERROR"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:10]
            + '"[${PROJECT_NAME}] Error : unknown build type ${CMAKE_BUILD_TYPE}")'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "endif()"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "endif()"
            + Common.LINE_BREAK[:1]
            + "endif()"
            + Common.LINE_BREAK[:2]
        )
        return generation
