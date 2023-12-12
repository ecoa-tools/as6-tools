# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module Source generation class.
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


class ModuleSourceGenerator:
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
        ext = ".c" + Common.switch_lang("", "pp", self._language)
        file_name = self._module_impl_name + ext
        file_path = os.path.join(self._path, "src", file_name)
        try:
            with open(file_path, "x") as f:
                indent_level = 0
                indent_step = 3
                generator = ModuleGenerator(indent_level, indent_step, True)
                visitor = ModuleVisitor(generator)
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        "Source Code for Module " + self._module_impl_name,
                    )
                )
                # Include
                f.write(
                    '#include "'
                    + self._module_impl_name
                    + ".h"
                    + Common.switch_lang("", "pp", self._language)
                    + '"'
                    + Common.LINE_BREAK[:2]
                )

                if self._language == "c++":
                    f.write(
                        Common.generate_open_namespace(self._module_impl_name)
                        + 'extern "C" {'
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                        + "Module* "
                        + self._module_impl_name
                        + "__new_instance()"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                        + "{"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (indent_level + 2 * indent_step)]
                        + "return new Module();"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                        + "}"
                        + Common.LINE_BREAK[:1]
                        + "}"
                        + Common.LINE_BREAK[:2]
                    )

                # Event functions
                events_received = self._ecoa_model.events_received.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if events_received:
                    f.write("/* Event operation handlers */" + Common.LINE_BREAK[:1])
                    f.write("/* ")
                    for comment in self._service_comment_helper.find_all("EventReceived"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for received in events_received:
                        f.write(received.accept(visitor))

                # Request-Response functions
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
                    f.write("/* Request-Response operation handlers */" + Common.LINE_BREAK[:1])
                    f.write("/* ")
                    for comment in self._service_comment_helper.find_all("ResquestResponse"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for received in requests_received:
                        f.write(received.accept(visitor))
                    for send in requests_send:
                        f.write(send.accept(visitor))

                # Error notification function
                module_impl = self._ecoa_model.module_impls.get(
                    self._component_impl_name + ":" + self._module_impl_name
                )
                module_type = self._ecoa_model.module_types.get(
                    self._component_impl_name + ":" + module_impl.module_type
                )
                if module_type.is_fault_handler:
                    f.write("// * Fault handler API:" + Common.LINE_BREAK[:2])
                    f.write(generator.error_notification.generate((self._module_impl_name, self._language)))

                # Versioned Data functions
                data_read = [
                    read
                    for read in self._ecoa_model.data_read.get(
                        self._component_impl_name + ":" + self._module_impl_name, []
                    )
                    if read.notifying
                ]
                if data_read:
                    f.write("/* Versioned Data Notifying operation handlers */" + Common.LINE_BREAK[:1])
                    f.write("/* ")
                    for comment in self._service_comment_helper.find_all("Data"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for read in data_read:
                        f.write(read.accept(visitor))

                # Lifecycle functions
                f.write("/* Lifecycle operation handlers */" + Common.LINE_BREAK[:2])
                lifecycle_state = ["INITIALIZE", "START", "STOP", "SHUTDOWN"]
                for state in lifecycle_state:
                    f.write(
                        "/**"
                        + Common.LINE_BREAK[:1]
                        + " * @internal	The callback to handle "
                        + self._module_impl_name
                        + " module on "
                        + state
                        + "."
                        + Common.LINE_BREAK[:1]
                    )
                    if self._language == "c":
                        f.write(
                            " * @param[in]	context	The "
                            + self._module_impl_name
                            + " module context."
                            + Common.LINE_BREAK[:1]
                        )
                    f.write(
                        " */"
                        + Common.LINE_BREAK[:1]
                        + "void"
                        + Common.LINE_BREAK[:1]
                        + Common.switch_lang(self._module_impl_name + "__", "Module::", self._language)
                        + state
                        + "__received ("
                        + Common.LINE_BREAK[:1]
                    )
                    if self._language == "c":
                        f.write(
                            Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                            + self._module_impl_name
                            + "__context * context"
                            + Common.LINE_BREAK[:1]
                        )
                    f.write(")" + Common.LINE_BREAK[:1] + "{" + Common.LINE_BREAK[:1])
                    if self._language == "c":
                        f.write(
                            Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                            + "(void) context;"
                            + Common.LINE_BREAK[:1]
                        )
                    f.write(
                        Common.SPACE_INDENTATION[: (indent_level + indent_step)]
                        + "// Insert logic here."
                        + Common.LINE_BREAK[:1]
                        + "}"
                        + Common.LINE_BREAK[: (1 + int(state != lifecycle_state[-1]))]
                    )
                if self._language == "c++":
                    f.write(Common.generate_close_namespace(self._module_impl_name, nb_line_break=1))
                logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
