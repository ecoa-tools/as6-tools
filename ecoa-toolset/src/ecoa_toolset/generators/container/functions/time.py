# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Time generation classes.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import Time


class TimeGenerator(FunctionGenerator):
    """"""

    type: str = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, type: str):
        super().__init__(indent_level, indent_step, body)
        self.type = type

    def _generate_prototype(self, element: Time) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + (
                "void"
                if self.type == "relative_local"
                else "ECOA" + Common.switch_lang("__", "::", element.language) + "return_status"
            )
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += "get_" + self.type + "_time (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if element.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + element.module_impl_name
                + "__context * context,"
                + Common.LINE_BREAK[:1]
            )
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + ("hr" if self.type == "relative_local" else "global")
            + "_time "
            + Common.switch_lang("*", "&", element.language)
            + " "
            + self.type.lower()
            + "_time"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Time) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            (
                "(void) context;"
                + Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "struct timespec ts;"
                + Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "#if defined(__unix__)"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "int result = clock_gettime (CLOCK_"
                + ("MONOTONIC" if self.type == "relative_local" else "REALTIME")
                + ", & ts);"
                + Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "if (result == -1)"
            ),
            (
                "std::chrono::"
                + ("steady" if self.type == "relative_local" else "system")
                + "_clock::time_point tp = std::chrono::"
                + ("steady" if self.type == "relative_local" else "system")
                + "_clock::now();"
            ),
            element.language,
        )
        generation += Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            (
                "{"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + "return"
                + (" ECOA__return_status_OPERATION_NOT_AVAILABLE" if self.type != "relative_local" else "")
                + ";"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "}"
                + Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "#else"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "if (timespec_get(&ts, TIME_UTC) != TIME_UTC) {"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + "return"
                + (" ECOA__return_status_OPERATION_NOT_AVAILABLE" if self.type != "relative_local" else "")
                + ";"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "}"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "#endif"
            ),
            (
                "std::chrono::"
                + ("steady" if self.type == "relative_local" else "system")
                + "_clock::duration dtn = tp.time_since_epoch();"
            ),
            element.language,
        )
        generation += Common.LINE_BREAK[:2] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            self.type.lower() + "_time->seconds = (ECOA__uint32) ts.tv_sec;",
            self.type.lower() + "_time.seconds = static_cast < ECOA::uint32 > (dtn.count());",
            element.language,
        )
        generation += Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            self.type.lower() + "_time->nanoseconds = (ECOA__uint32) ts.tv_nsec;",
            (
                self.type.lower()
                + "_time.nanoseconds = static_cast < ECOA::uint32 > "
                + "(std::chrono::duration_cast < std::chrono::nanoseconds > (dtn).count());"
            ),
            element.language,
        )
        if self.type != "relative_local":
            generation += (
                Common.LINE_BREAK[:2]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "return ECOA"
                + Common.switch_lang("__", "::", element.language)
                + "return_status"
                + Common.switch_lang("_OK", "()", element.language)
                + ";"
            )
        return generation


class TimeResolutionGenerator(FunctionGenerator):
    """"""

    type: str = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, type: str):
        super().__init__(indent_level, indent_step, body)
        self.type = type

    def _generate_prototype(self, element: Time) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "void"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += "get_" + self.type + "_time_resolution (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        if element.language == "c":
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + element.module_impl_name
                + "__context * context,"
                + Common.LINE_BREAK[:1]
            )
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "duration "
            + Common.switch_lang("*", "&", element.language)
            + " "
            + self.type.lower()
            + "_time_resolution"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Time) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        if element.language == "c":
            generation += "(void) context;" + Common.LINE_BREAK[:2] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += (
            "struct timespec ts;"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "#if defined(__unix__)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "int result = clock_getres (CLOCK_"
            + ("MONOTONIC" if self.type == "relative_local" else "REALTIME")
            + ", & ts);"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (result == -1)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "return;" + Common.LINE_BREAK[:1]
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "#else"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "struct timespec ts1, ts2;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "int result = timespec_get(&ts1, TIME_UTC);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (result != TIME_UTC)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "return;" + Common.LINE_BREAK[:1]
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "do"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "result = timespec_get(&ts2, TIME_UTC);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (result != TIME_UTC)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "return;" + Common.LINE_BREAK[:1]
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "} while(ts1.tv_sec == ts2.tv_sec && ts1.tv_nsec == ts2.tv_nsec);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ts.tv_sec = ts2.tv_sec - ts1.tv_sec;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "long double tmp = (long double) ts.tv_sec + ((ts2.tv_nsec - ts1.tv_nsec) * 1E-9);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (ts1.tv_nsec > ts2.tv_nsec)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "ts.tv_sec--;" + Common.LINE_BREAK[:1]
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ts.tv_nsec = (long) ((tmp - (long double) ts.tv_sec) * 1E9);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "#endif"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            self.type.lower() + "_time_resolution->seconds = (ECOA__uint32) ts.tv_sec;",
            self.type.lower() + "_time_resolution.seconds = static_cast < ECOA::uint32 > (ts.tv_sec);",
            element.language,
        )
        generation += Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level]
        generation += Common.switch_lang(
            self.type.lower() + "_time_resolution->nanoseconds = (ECOA__uint32) ts.tv_nsec;",
            self.type.lower() + "_time_resolution.nanoseconds = static_cast < ECOA::uint32 > (ts.tv_nsec);",
            element.language,
        )
        return generation


class TimeServicesGenerator:
    """"""

    relative_local_time: TimeGenerator = None
    utc_time: TimeGenerator = None
    absolute_system_time: TimeGenerator = None
    relative_local_time_resolution: TimeResolutionGenerator = None
    utc_time_resolution: TimeResolutionGenerator = None
    absolute_system_time_resolution: TimeResolutionGenerator = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        self.relative_local_time = TimeGenerator(indent_level, indent_step, body, "relative_local")
        self.utc_time = TimeGenerator(indent_level, indent_step, body, "UTC")
        self.absolute_system_time = TimeGenerator(indent_level, indent_step, body, "absolute_system")
        self.relative_local_time_resolution = TimeResolutionGenerator(indent_level, indent_step, body, "relative_local")
        self.utc_time_resolution = TimeResolutionGenerator(indent_level, indent_step, body, "UTC")
        self.absolute_system_time_resolution = TimeResolutionGenerator(
            indent_level, indent_step, body, "absolute_system"
        )
