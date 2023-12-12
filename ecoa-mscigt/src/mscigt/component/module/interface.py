# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module Interface generation class.
"""

# Standard library imports
import logging
import os

# Local imports
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.module.generator import ModuleGenerator
from ecoa_toolset.models.helpers.service_comment import ServiceCommentHelper
from ecoa_toolset.visitors.module import ModuleVisitor

logger = logging.getLogger(__name__)


class ModuleInterfaceGenerator:
    """"""

    _ecoa_model = None
    _path: str = None
    _component_impl_name: str = None
    _module_impl_name: str = None
    _language: str = None
    _templates: Templates = None
    _service_comment_helper = None

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
        self._service_comment_helper = ServiceCommentHelper(self._ecoa_model)

    def generate(self) -> None:
        """Writes the module interface header code."""
        ext = ".h" + Common.switch_lang("", "pp", self._language)
        file_name = self._module_impl_name + ext
        file_path = os.path.join(self._path, "inc-gen", file_name)
        module_impl = self._ecoa_model.module_impls.get(self._component_impl_name + ":" + self._module_impl_name)
        module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
        try:
            with open(file_path, "x") as f:
                indent_level = Common.switch_lang(0, 5, self._language)
                indent_step = Common.switch_lang(2, 3, self._language)
                generator = ModuleGenerator(indent_level, indent_step, False)
                visitor = ModuleVisitor(generator)
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        "Header for Module " + self._module_impl_name,
                        file_unmodifiable=True,
                    )
                )
                f.write(Common.generate_header_open_guard(self._module_impl_name, self._language))

                # Includes
                f.write("/* Standard Types */" + Common.LINE_BREAK[:1])
                f.write("#include <ECOA.h" + ("pp" if self._language == "c++" else "") + ">" + Common.LINE_BREAK[:2])
                f.write("/* Additionally created types */" + Common.LINE_BREAK[:1])
                f.write(Common.generate_includes(self._ecoa_model.use[self._component_impl_name], self._language))
                f.write("/* Include container header */" + Common.LINE_BREAK[:1])
                f.write(
                    '#include "'
                    + self._module_impl_name
                    + "_container.h"
                    + ("pp" if self._language == "c++" else "")
                    + '"'
                    + Common.LINE_BREAK[:1]
                )
                f.write("/* Include container types */" + Common.LINE_BREAK[:1])
                f.write(
                    '#include "'
                    + self._module_impl_name
                    + "_container_types.h"
                    + ("pp" if self._language == "c++" else "")
                    + '"'
                    + Common.LINE_BREAK[:1]
                )
                if self._language == "c":
                    f.write(Common.LINE_BREAK[:1])
                elif self._language == "c++":
                    f.write(
                        "/* Include user context */"
                        + Common.LINE_BREAK[:1]
                        + '#include "'
                        + self._module_impl_name
                        + '_user_context.hpp"'
                        + Common.LINE_BREAK[:2]
                        + Common.generate_open_namespace(self._module_impl_name)
                        + "class Module {"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[:2]
                        + "public:"
                        + Common.LINE_BREAK[:2]
                    )
                # Lifecycle function prototype
                f.write(
                    Common.SPACE_INDENTATION[:indent_level]
                    + "/* Lifecycle operation handlers specifications */"
                    + Common.LINE_BREAK[:2]
                )
                lifecycle_state = ["INITIALIZE", "START", "STOP", "SHUTDOWN"]
                for state in lifecycle_state:
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "void" + Common.LINE_BREAK[:1])
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + Common.switch_lang(self._module_impl_name + "__", "", self._language)
                    )
                    f.write(state + "__received (" + Common.LINE_BREAK[:1])
                    if self._language == "c":
                        f.write(
                            Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                            + self._module_impl_name
                            + "__context * context"
                            + Common.LINE_BREAK[:1]
                        )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + ");" + Common.LINE_BREAK[:2])

                if self._language == "c++":
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// the Module Implementation shall hold a Container pointer"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// which is passed within the constructor"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:5] + "Container* container;" + Common.LINE_BREAK[:2])

                    if module_type.has_user_context:
                        f.write(
                            Common.SPACE_INDENTATION[:5]
                            + "// Optional user data (which does not belong to the warm start context)"
                            + Common.LINE_BREAK[:1]
                        )
                        f.write(
                            Common.SPACE_INDENTATION[:5]
                            + "// for this module implementation may be declared here within a standard"
                            + Common.LINE_BREAK[:1]
                        )
                        f.write(Common.SPACE_INDENTATION[:5] + "// structure:" + Common.LINE_BREAK[:1])
                        f.write(Common.SPACE_INDENTATION[:5] + "user_context user;" + Common.LINE_BREAK[:2])

                    if module_type.has_warm_start_context:
                        f.write(
                            Common.SPACE_INDENTATION[:5]
                            + "// Optional Warm Start data for this module implementation may be declared"
                            + Common.LINE_BREAK[:1]
                        )
                        f.write(
                            Common.SPACE_INDENTATION[:5]
                            + "// here as a single attribute named warm_start which may be of a user"
                            + Common.LINE_BREAK[:1]
                        )
                        f.write(Common.SPACE_INDENTATION[:5] + "// defined type." + Common.LINE_BREAK[:1])
                        f.write(Common.SPACE_INDENTATION[:5] + "warm_start_context warm_start;" + Common.LINE_BREAK[:2])

                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// The following describes the API generated:"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Event: event_received operations"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Request-Response: request_received operations"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Asynchronous Request-Response: response_received operation"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Notifying Versioned Data Read: updated operation"
                        + Common.LINE_BREAK[:2]
                    )

                # Event function prototype
                events_received = self._ecoa_model.events_received.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if events_received:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Event operation handlers specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("EventReceived"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for received in events_received:
                        f.write(received.accept(visitor))

                # Request-Response function prototype
                requests_received = self._ecoa_model.requests_received.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                requests_send = [
                    send
                    for send in self._ecoa_model.requests_send.get(
                        self._component_impl_name + ":" + self._module_impl_name, []
                    )
                    if not send.is_synchronous
                ]
                if requests_received or requests_send:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Request-Response operation handlers specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("ResquestResponse"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for received in requests_received:
                        f.write(received.accept(visitor))
                    for send in requests_send:
                        f.write(send.accept(visitor))

                # Versioned Data function prototype
                data_read = [
                    read
                    for read in self._ecoa_model.data_read.get(
                        self._component_impl_name + ":" + self._module_impl_name, []
                    )
                    if read.notifying
                ]
                if data_read:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Versioned Data Notifying operation handlers specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("Data"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for read in data_read:
                        f.write(read.accept(visitor))

                # Error notification function prototype
                module_impl = self._ecoa_model.module_impls.get(
                    self._component_impl_name + ":" + self._module_impl_name
                )
                module_type = self._ecoa_model.module_types.get(
                    self._component_impl_name + ":" + module_impl.module_type
                )
                if module_type.is_fault_handler is True:
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "// * Fault handler API:" + Common.LINE_BREAK[:2])
                    f.write(generator.error_notification.generate((self._module_impl_name, self._language)))

                if self._language == "c++":
                    f.write(
                        "}; /* Module */"
                        + Common.LINE_BREAK[:2]
                        + 'extern "C" {'
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[:2]
                        + "Module* "
                        + self._module_impl_name
                        + "__new_instance();"
                        + Common.LINE_BREAK[:1]
                        + "}"
                        + Common.LINE_BREAK[:2]
                        + Common.generate_close_namespace(self._module_impl_name)
                    )
                # Close guard
                f.write(Common.generate_header_close_guard(self._module_impl_name, self._language))
                logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
