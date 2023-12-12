# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""  Module unit tests main source code generation.
"""

# Standard library imports
import logging
import os
from typing import Any, Dict, List

# Local imports
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.helpers.platform_hook import PlatformHook, PlatformHookHelper
from ecoa_toolset.models.components import DataRead, EventReceived, Parameter, RequestReceived, RequestSend
from ecoa_toolset.models.ecoa_objects.ecoa_types_2_0 import Simple
from ecoa_toolset.models.visitor import Visitor

logger = logging.getLogger(__name__)


class ModuleTestImplementationVisitor(Visitor):
    """Visit ECOA components for generates a module test source code."""

    _language: str = None
    _hooks: Dict[str, PlatformHook] = None
    _data_updated_generated: List[str] = None
    _event_received_generated: List[str] = None
    _request_received_generated: List[str] = None
    _response_received_generated: List[str] = None

    def __init__(self, language, hooks):
        self._language = language
        self._hooks = hooks
        self._data_updated_generated = []
        self._event_received_generated = []
        self._request_received_generated = []
        self._response_received_generated = []

    def _generate_test_function_prototype(self, element: Any, operation_type: str) -> str:
        generation = (
            "void"
            + Common.LINE_BREAK[:1]
            + "test__"
            + element.module_impl_name
            + "__"
            + element.name
            + "__"
            + operation_type
            + "(void)"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_test_function_body_before_test(self) -> str:
        generation = (
            "{"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "before_test(__FUNCTION__, __LINE__);"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_test_function_body_operation_init_parameters(self, parameters: List) -> str:
        generation = ""
        if parameters:
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "/* Module operation input"
                + ("s" if len(parameters) > 1 else "")
                + "; to be initialized */"
                + Common.LINE_BREAK[:1]
            )
        for parameter in parameters:
            generation += (
                Common.SPACE_INDENTATION[:3]
                + ""
                + Common.construct_complete_variable_type(parameter, self._language)
                + " "
                + parameter.name
                + ";"
                + Common.LINE_BREAK[:1]
            )
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_test_function_body_operation_call_parameters(self, parameters: List) -> str:
        generation = ""
        for i, parameter in enumerate(parameters):
            generation += (
                Common.SPACE_INDENTATION[:6]
                + ("&" if getattr(parameter.type_category, "is_complex", "") and self._language == "c" else "")
                + parameter.name
                + ("," if i != len(parameters) - 1 else "")
                + Common.LINE_BREAK[:1]
            )
        return generation

    def _generate_test_function_body_operation_call(
        self, element: Any, operation_type: str, parameters: List = []
    ) -> str:
        generation = (
            Common.SPACE_INDENTATION[:3] + "/* Module operation call; do not modify here */" + Common.LINE_BREAK[:1]
        )
        for hook in self._hooks.values():
            for component_name in hook.component_names:
                generation += (
                    Common.SPACE_INDENTATION[:3]
                    + Common.switch_lang(
                        hook.module_impl_name + "__",
                        hook.module_inst_name + "_" + component_name + "_Module.",
                        self._language,
                    )
                    + element.name
                    + "__"
                    + operation_type
                    + "("
                    + Common.LINE_BREAK[:1]
                    + Common.switch_lang(
                        Common.SPACE_INDENTATION[:6]
                        + "&"
                        + hook.module_inst_name
                        + "_"
                        + component_name
                        + "_Context"
                        + ("," if parameters else "")
                        + Common.LINE_BREAK[:1],
                        "",
                        self._language,
                    )
                    + self._generate_test_function_body_operation_call_parameters(parameters)
                    + Common.SPACE_INDENTATION[:3]
                    + ");"
                    + Common.LINE_BREAK[:1]
                )
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_test_function_body_after_test(self) -> str:
        generation = (
            Common.SPACE_INDENTATION[:3]
            + "/* Insert test logic here. e.g: assert(1 == 2) */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "after_test();"
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def visit_data_read(self, element: DataRead) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._data_updated_generated:
            self._data_updated_generated.append(key)
            generation += self._generate_test_function_prototype(element, "updated")
            generation += self._generate_test_function_body_before_test()
            generation += self._generate_test_function_body_operation_call(element, "updated")
            generation += self._generate_test_function_body_after_test()
        return generation

    def visit_event_received(self, element: EventReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._event_received_generated:
            self._event_received_generated.append(key)
            generation += self._generate_test_function_prototype(element, "received")
            generation += self._generate_test_function_body_before_test()
            generation += self._generate_test_function_body_operation_init_parameters(element.inputs)
            generation += self._generate_test_function_body_operation_call(element, "received", element.inputs)
            generation += self._generate_test_function_body_after_test()
        return generation

    def visit_request_received(self, element: RequestReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._request_received_generated:
            self._request_received_generated.append(key)
            generation += self._generate_test_function_prototype(element, "request_received")
            generation += self._generate_test_function_body_before_test()
            generation += self._generate_test_function_body_operation_init_parameters(element.inputs)
            generation += self._generate_test_function_body_operation_call(element, "request_received", element.inputs)
            generation += self._generate_test_function_body_after_test()
        return generation

    def visit_request_send(self, element: RequestSend) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._response_received_generated:
            self._response_received_generated.append(key)
            generation += self._generate_test_function_prototype(element, "response_received")
            generation += self._generate_test_function_body_before_test()
            parameters = [
                Parameter("ID", "ECOA", "uint32", Simple()),
                Parameter("status", "ECOA", "return_status", Simple()),
            ] + element.outputs
            generation += self._generate_test_function_body_operation_init_parameters(parameters)
            generation += self._generate_test_function_body_operation_call(element, "response_received", parameters)
            generation += self._generate_test_function_body_after_test()
        return generation


class ModuleTestPrototypeVisitor(Visitor):
    """Visit ECOA components for generates a module test source code."""

    _data_updated_generated: List[str] = None
    _event_received_generated: List[str] = None
    _request_received_generated: List[str] = None
    _response_received_generated: List[str] = None

    def __init__(self):
        self._data_updated_generated = []
        self._event_received_generated = []
        self._request_received_generated = []
        self._response_received_generated = []

    def visit_data_read(self, element: DataRead) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._data_updated_generated:
            self._data_updated_generated.append(key)
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + element.module_impl_name
                + "__"
                + element.name
                + "__updated();"
                + Common.LINE_BREAK[:1]
            )
        return generation

    def visit_event_received(self, element: EventReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._event_received_generated:
            self._event_received_generated.append(key)
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + element.module_impl_name
                + "__"
                + element.name
                + "__received();"
                + Common.LINE_BREAK[:1]
            )
        return generation

    def visit_request_received(self, element: RequestReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._request_received_generated:
            self._request_received_generated.append(key)
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + element.module_impl_name
                + "__"
                + element.name
                + "__request_received();"
                + Common.LINE_BREAK[:1]
            )
        return generation

    def visit_request_send(self, element: RequestSend) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._response_received_generated:
            self._response_received_generated.append(key)
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + element.module_impl_name
                + "__"
                + element.name
                + "__response_received();"
                + Common.LINE_BREAK[:1]
            )
        return generation


class UnitTestMainGenerator:
    """"""

    _ecoa_model = None
    _path: str = None
    _component_impl_name: str = None
    _module_impl_name: str = None
    _language: str = None
    _templates: Templates = None
    _hooks: Dict[str, PlatformHook] = None

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
        self._hooks = PlatformHookHelper(self._ecoa_model).find_all(
            component_impl_name=self._component_impl_name, module_impl_name=self._module_impl_name
        )

    def _generate_module_fault_handler_test_call(self) -> str:
        sep = Common.switch_lang("__", "::", self._language)
        generation = (
            Common.SPACE_INDENTATION[:3] + "/* Module operation inputs; can be modified */" + Common.LINE_BREAK[:1]
        )
        if "c++" == self._language:
            generation += Common.SPACE_INDENTATION[:3] + "ECOA::error_id error_id = 0;" + Common.LINE_BREAK[:1]
        generation += (
            Common.SPACE_INDENTATION[:3]
            + "const ECOA"
            + sep
            + "global_time timestamp = {0, 0};"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "ECOA"
            + sep
            + "asset_id asset_id = 0;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "ECOA"
            + sep
            + "asset_type asset_type = ECOA"
            + sep
            + "asset_type"
            + Common.switch_lang("_", "::", self._language)
            + "COMPONENT;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "ECOA"
            + sep
            + "error_type error_type = ECOA"
            + sep
            + "error_type"
            + Common.switch_lang("_", "::", self._language)
            + "RESOURCE_NOT_AVAILABLE;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "ECOA"
            + sep
            + "error_code error_code = 0;"
            + Common.LINE_BREAK[:2]
        )
        generation += (
            Common.SPACE_INDENTATION[:3] + "/* Module operation call; do not modify here */" + Common.LINE_BREAK[:1]
        )
        for hook in self._hooks.values():
            for component_name in hook.component_names:
                generation += (
                    Common.SPACE_INDENTATION[:3]
                    + Common.switch_lang(
                        hook.module_impl_name + "__",
                        hook.module_inst_name + "_" + component_name + "_Module.",
                        self._language,
                    )
                    + "error_notification("
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + Common.switch_lang(
                        "&" + hook.module_inst_name + "_" + component_name + "_Context", "error_id", self._language
                    )
                    + ","
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + Common.switch_lang("&", "", self._language)
                    + "timestamp,"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + "asset_id,"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + "asset_type,"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + "error_type,"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:6]
                    + "error_code"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:3]
                    + ");"
                    + Common.LINE_BREAK[:1]
                )
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_module_fault_handler_test(self) -> str:
        """Writes the module interface for the error_notification at Fault Handler level."""
        generation = (
            "void"
            + Common.LINE_BREAK[:1]
            + "test__"
            + self._module_impl_name
            + "__error_notification(void)"
            + Common.LINE_BREAK[:1]
            + "{"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "before_test(__FUNCTION__, __LINE__);"
            + Common.LINE_BREAK[:2]
        )
        generation += self._generate_module_fault_handler_test_call()
        generation += (
            Common.SPACE_INDENTATION[:3]
            + "/* Insert test logic here. e.g: assert(1 == 2) */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "after_test();"
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_standard_includes(self) -> str:
        generation = "/* Standards libraries */" + Common.LINE_BREAK[:1]
        libraries = ["time", "stdio", "string", "stdarg"]
        for library in libraries:
            generation += "#include <" + library + ".h>" + Common.LINE_BREAK[:1]
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_module_includes(self) -> str:
        generation = (
            "/* Module interface */"
            + Common.LINE_BREAK[:1]
            + '#include "'
            + self._module_impl_name
            + ".h"
            + ("pp" if self._language == "c++" else "")
            + '"'
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_utilities_variables(self) -> str:
        generation = (
            "/* Override assert macro for unit test purpose */"
            + Common.LINE_BREAK[:1]
            + "#ifdef assert"
            + Common.LINE_BREAK[:1]
            + "#undef assert"
            + Common.LINE_BREAK[:1]
            + "#endif"
            + Common.LINE_BREAK[:1]
            + "#define assert(x) (test_result = test_result & (x))"
            + Common.LINE_BREAK[:2]
            + "static int test_result;"
            + Common.LINE_BREAK[:1]
            + "static int nb_tests = 0;"
            + Common.LINE_BREAK[:1]
            + "static int nb_tests_failed = 0;"
            + Common.LINE_BREAK[:1]
            + "static int nb_tests_passed = 0;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_externs(self) -> str:
        generation = ""
        for hook in self._hooks.values():
            for component_name in hook.component_names:
                if "c++" == hook.language.lower():
                    generation += (
                        "extern "
                        + hook.module_impl_name
                        + "::Module "
                        + hook.module_inst_name
                        + "_"
                        + component_name
                        + "_Module;"
                        + Common.LINE_BREAK[:1]
                    )
                if "c" == hook.language.lower():
                    generation += (
                        "extern "
                        + hook.module_impl_name
                        + "__context "
                        + hook.module_inst_name
                        + "_"
                        + component_name
                        + "_Context;"
                        + Common.LINE_BREAK[:1]
                    )
        if generation:
            generation += Common.LINE_BREAK[:1]
        generation += "extern void cm_initialize(void);" + Common.LINE_BREAK[:1]
        if self._ecoa_model.pinfos.get(self._component_impl_name + ":" + self._module_impl_name, []):
            generation += "extern void cm_shutdown(void);" + Common.LINE_BREAK[:1]
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_unit_test_utilities_function(self) -> str:
        generation = (
            "/* Unit test utilities */"
            + Common.LINE_BREAK[:2]
            + "void"
            + Common.LINE_BREAK[:1]
            + "before_test"
            + "(const char *test_name, const int line)"
            + Common.LINE_BREAK[:1]
            + "{"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "test_result = 1;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + 'printf("%s:%d: %s() ", __FILE__, line, test_name);'
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:2]
            + "void"
            + Common.LINE_BREAK[:1]
            + "after_test"
            + "(void)"
            + Common.LINE_BREAK[:1]
            + "{"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "nb_tests++;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "if (test_result)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:5]
            + "nb_tests_passed++;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "else"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:5]
            + "nb_tests_failed++;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + 'printf("%s\\n", test_result ? "PASSED" : "FAILED");'
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def _generate_ecoa_lifecycle_function_test_call(self, state: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[:3] + "/* Module operation call; do not modify here */" + Common.LINE_BREAK[:1]
        )
        for hook in self._hooks.values():
            for component_name in hook.component_names:
                generation += (
                    Common.SPACE_INDENTATION[:3]
                    + Common.switch_lang(
                        hook.module_impl_name + "__",
                        hook.module_inst_name + "_" + component_name + "_Module.",
                        self._language,
                    )
                    + state
                    + "__received("
                    + Common.switch_lang(
                        "&" + hook.module_inst_name + "_" + component_name + "_Context", "", self._language
                    )
                    + ");"
                    + Common.LINE_BREAK[:1]
                )
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_ecoa_lifecycle_function_test(self) -> str:
        generation = "/* Lifecycle operation tests */" + Common.LINE_BREAK[:2]
        lifecycle_state = ["INITIALIZE", "START", "STOP", "SHUTDOWN"]
        for state in lifecycle_state:
            generation += (
                "void"
                + Common.LINE_BREAK[:1]
                + "test__"
                + self._module_impl_name
                + "__"
                + state
                + "(void)"
                + Common.LINE_BREAK[:1]
                + "{"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[:3]
                + "before_test(__FUNCTION__, __LINE__);"
                + Common.LINE_BREAK[:2]
            )
            generation += self._generate_ecoa_lifecycle_function_test_call(state)
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "/* Insert test logic here. e.g: assert(1 == 2) */"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[:3]
                + "after_test();"
                + Common.LINE_BREAK[:1]
                + "}"
                + Common.LINE_BREAK[:2]
            )
        return generation

    def _generate_all_test(self) -> str:
        visitor = ModuleTestImplementationVisitor(self._language, self._hooks)
        generation = self._generate_unit_test_utilities_function()
        generation += self._generate_ecoa_lifecycle_function_test()
        # Event functions
        events_received = self._ecoa_model.events_received.get(
            self._component_impl_name + ":" + self._module_impl_name, []
        )
        if events_received:
            generation += "/* Event operation tests */" + Common.LINE_BREAK[:2]
            for received in events_received:
                generation += received.accept(visitor)
        # Request-Response functions
        requests_received = self._ecoa_model.requests_received.get(
            self._component_impl_name + ":" + self._module_impl_name, []
        )
        requests_send = [
            send
            for send in self._ecoa_model.requests_send.get(self._component_impl_name + ":" + self._module_impl_name, [])
            if not send.is_synchronous
        ]
        if requests_received or requests_send:
            generation += "/* Request-Response operation tests */" + Common.LINE_BREAK[:2]
            for received in requests_received:
                generation += received.accept(visitor)
            for send in requests_send:
                generation += send.accept(visitor)
        # Fault handler API
        mi = self._ecoa_model.module_impls.get(self._component_impl_name + ":" + self._module_impl_name)
        mt = self._ecoa_model.module_types.get(self._component_impl_name + ":" + mi.module_type)
        if mt.is_fault_handler:
            generation += "/* Fault handler operation test */" + Common.LINE_BREAK[:2]
            generation += self._generate_module_fault_handler_test()
        # Versioned data functions
        data_read = [
            read
            for read in self._ecoa_model.data_read.get(self._component_impl_name + ":" + self._module_impl_name, [])
            if read.notifying
        ]
        if data_read:
            generation += "/* Versioned data operation tests */" + Common.LINE_BREAK[:2]
            for read in data_read:
                generation += read.accept(visitor)
        return generation

    def _generate_main_function(self) -> str:
        visitor = ModuleTestPrototypeVisitor()
        generation = (
            "/* main */"
            + Common.LINE_BREAK[:2]
            + "int"
            + Common.LINE_BREAK[:1]
            + "main"
            + "(void)"
            + Common.LINE_BREAK[:1]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        # CM Initialize function
        generation += (
            Common.SPACE_INDENTATION[:3]
            + "/* Initialize container mock */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "cm_initialize();"
            + Common.LINE_BREAK[:1]
        )
        # Lifecycle operations
        generation += Common.SPACE_INDENTATION[:3] + "/* Lifecycle operation tests */" + Common.LINE_BREAK[:1]
        lifecycle_state = ["INITIALIZE", "START", "STOP", "SHUTDOWN"]
        for state in lifecycle_state:
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + self._module_impl_name
                + "__"
                + state
                + "();"
                + Common.LINE_BREAK[:1]
            )
        # Event functions
        events_received = self._ecoa_model.events_received.get(
            self._component_impl_name + ":" + self._module_impl_name, []
        )
        if events_received:
            generation += Common.SPACE_INDENTATION[:3] + "/* Event operation tests */" + Common.LINE_BREAK[:1]
            for received in events_received:
                generation += received.accept(visitor)
        # Request-Response functions
        requests_received = self._ecoa_model.requests_received.get(
            self._component_impl_name + ":" + self._module_impl_name, []
        )
        requests_send = [
            send
            for send in self._ecoa_model.requests_send.get(self._component_impl_name + ":" + self._module_impl_name, [])
            if not send.is_synchronous
        ]
        if requests_received or requests_send:
            generation += (
                Common.SPACE_INDENTATION[:3] + "/* Request-Response operation tests */" + Common.LINE_BREAK[:1]
            )
            for received in requests_received:
                generation += received.accept(visitor)
            for send in requests_send:
                generation += send.accept(visitor)
        # Fault handler API
        mi = self._ecoa_model.module_impls.get(self._component_impl_name + ":" + self._module_impl_name)
        mt = self._ecoa_model.module_types.get(self._component_impl_name + ":" + mi.module_type)
        if mt.is_fault_handler is True:
            generation += Common.SPACE_INDENTATION[:3] + "/* Fault handler operation test */" + Common.LINE_BREAK[:1]
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "test__"
                + self._module_impl_name
                + "__error_notification();"
                + Common.LINE_BREAK[:1]
            )
        # Versioned data functions
        data_read = [
            read
            for read in self._ecoa_model.data_read.get(self._component_impl_name + ":" + self._module_impl_name, [])
            if read.notifying
        ]
        if data_read:
            generation += Common.SPACE_INDENTATION[:3] + "/* Versioned data operation tests */" + Common.LINE_BREAK[:1]
            for read in data_read:
                generation += read.accept(visitor)
        # CM Shutdown function
        if self._ecoa_model.pinfos.get(self._component_impl_name + ":" + self._module_impl_name, []):
            generation += (
                Common.SPACE_INDENTATION[:3]
                + "/* Shutdown container mock */"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[:3]
                + "cm_shutdown();"
                + Common.LINE_BREAK[:1]
            )
        # Test summary
        generation += (
            Common.SPACE_INDENTATION[:3]
            + "/* Test summary */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + 'printf("Summary: %d failed, %d passed, %d total\\n", nb_tests_failed, nb_tests_passed, nb_tests);'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:3]
            + "return nb_tests_failed != 0;"
            + Common.LINE_BREAK[:1]
            + "}"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def generate(self):
        """Generates the unit test main file."""
        ext = ".c" + Common.switch_lang("", "pp", self._language)
        file_name = "main" + ext
        file_path = os.path.join(self._path, "tests", file_name)
        try:
            with open(file_path, "x") as f:
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        "Unit Test Code for Module " + self._module_impl_name,
                    )
                )
                f.write(self._generate_standard_includes())
                f.write(self._generate_module_includes())
                f.write(self._generate_utilities_variables())
                f.write(self._generate_externs())
                f.write(self._generate_all_test())
                f.write(self._generate_main_function())
            logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
