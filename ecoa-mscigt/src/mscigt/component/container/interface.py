# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Container Interface generation class.
"""

# Standard library imports
import logging
import os

# Local imports
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.container.generator import ContainerGenerator
from ecoa_toolset.models.helpers.service_comment import ServiceCommentHelper
from ecoa_toolset.visitors.container import ContainerVisitor

logger = logging.getLogger(__name__)


class ContainerInterfaceGenerator:
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

    def _generate_module_context_structure(self, module_type) -> str:
        """Generates the container interface header module context structure."""
        generation = (
            "/* Module Context structure declaration */\n"
            + "typedef struct\n{\n"
            + Common.SPACE_INDENTATION[:4]
            + "/*\n"
            + Common.SPACE_INDENTATION[:4]
            + " * Other container technical data will be accessible through the pointer\n"
            + Common.SPACE_INDENTATION[:4]
            + " * defined here\n"
            + Common.SPACE_INDENTATION[:4]
            + " */\n"
            + Common.SPACE_INDENTATION[:4]
            + "struct "
            + self._module_impl_name
            + "__platform_hook *platform_hook;"
            + Common.LINE_BREAK[:2]
        )
        if module_type.has_user_context:
            generation += (
                Common.SPACE_INDENTATION[:4]
                + "/* When the optional user context is used, the type\n"
                + Common.SPACE_INDENTATION[:4]
                + " * "
                + self._module_impl_name
                + "_user_context shall be defined by the user\n"
                + Common.SPACE_INDENTATION[:4]
                + " * in the "
                + self._module_impl_name
                + "_user_context.h file to carry the module\n"
                + Common.SPACE_INDENTATION[:4]
                + " * implementation private data\n"
                + Common.SPACE_INDENTATION[:4]
                + " */\n"
                + Common.SPACE_INDENTATION[:4]
                + self._module_impl_name
                + "_user_context user;"
                + Common.LINE_BREAK[:2]
            )
        if module_type.has_warm_start_context:
            generation += (
                Common.SPACE_INDENTATION[:4]
                + "/* When the optional warm start context is used, the type\n"
                + Common.SPACE_INDENTATION[:4]
                + " * "
                + self._module_impl_name
                + "_warm_start_context shall be defined by the user\n"
                + Common.SPACE_INDENTATION[:4]
                + " * in the "
                + self._module_impl_name
                + "_user_context.h file to carry the module\n"
                + Common.SPACE_INDENTATION[:4]
                + " * implementation private data\n"
                + Common.SPACE_INDENTATION[:4]
                + " */\n"
                + Common.SPACE_INDENTATION[:4]
                + self._module_impl_name
                + "_warm_start_context warm_start;"
                + Common.LINE_BREAK[:2]
            )
        generation += (
            "}"
            + Common.SPACE_INDENTATION[:3]
            + self._module_impl_name
            + "__context;"
            + Common.LINE_BREAK[:2]
            + "typedef "
            + self._module_impl_name
            + "__context "
            + self._module_impl_name
            + "_context;"
            + Common.LINE_BREAK[:2]
        )
        return generation

    def generate(self) -> None:
        """Generates the container interface header code."""
        ext = ".h" + Common.switch_lang("", "pp", self._language)
        file_type = "container"
        file_name = self._module_impl_name + "_" + file_type + ext
        file_path = os.path.join(self._path, "inc-gen", file_name)
        module_impl = self._ecoa_model.module_impls.get(self._component_impl_name + ":" + self._module_impl_name)
        module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
        try:
            with open(file_path, "x") as f:
                indent_level = Common.switch_lang(0, 5, self._language)
                indent_step = Common.switch_lang(2, 3, self._language)
                generator = ContainerGenerator(indent_level, indent_step, False, False)
                visitor = ContainerVisitor(generator)
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        file_type.replace("_", " ").title() + " header for Module " + self._module_impl_name,
                        file_unmodifiable=True,
                    )
                )

                f.write(Common.generate_header_open_guard(self._module_impl_name, self._language, file_type))

                # Includes
                f.write(
                    "#include " + Common.switch_lang("<stdio.h>", "<fstream>", self._language) + Common.LINE_BREAK[:1]
                )
                f.write(
                    "/* Standard Types */\n"
                    + "#include <ECOA.h"
                    + ("pp" if self._language == "c++" else "")
                    + ">"
                    + Common.LINE_BREAK[:2]
                    + "/* Additionally created types */\n"
                )
                f.write(Common.generate_includes(self._ecoa_model.use[self._component_impl_name], self._language))
                f.write(
                    "/* Container Types */\n"
                    + '#include "'
                    + self._module_impl_name
                    + "_container_types.h"
                    + ("pp" if self._language == "c++" else "")
                    + '"'
                    + Common.LINE_BREAK[:2]
                )
                if self._language == "c":
                    f.write(
                        "/* Optional User Context: the "
                        + self._module_impl_name
                        + "_user_context.h header\n"
                        + " * inclusion is optional (depends if user and/or warm start context\n"
                        + " * are being used\n"
                        + " */\n"
                        + '#include "'
                        + self._module_impl_name
                        + '_user_context.h"'
                        + Common.LINE_BREAK[:2]
                        + "/* Incomplete definition of the technical (platform-dependent) part of the */"
                        + Common.LINE_BREAK[:1]
                        + "/* context (it will be defined privately by the container) */"
                        + Common.LINE_BREAK[:1]
                        + "struct"
                        + Common.SPACE_INDENTATION[:1]
                        + self._module_impl_name
                        + "__platform_hook;"
                        + Common.LINE_BREAK[:2]
                        + self._generate_module_context_structure(module_type)
                    )
                elif self._language == "c++":
                    f.write(
                        Common.generate_open_namespace(self._module_impl_name)
                        + "class Container {"
                        + Common.LINE_BREAK[:2]
                        + Common.SPACE_INDENTATION[:2]
                        + "public:"
                        + Common.LINE_BREAK[:2]
                    )

                # Log functions prototypes
                log = self._ecoa_model.logs.get(self._component_impl_name + ":" + self._module_impl_name)
                if log:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Logging and fault management services API */"
                        + Common.LINE_BREAK[:2]
                    )
                    f.write(log.accept(visitor))

                # Time functions prototypes
                time = self._ecoa_model.times.get(self._component_impl_name + ":" + self._module_impl_name)
                if time:
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* Time services API */" + Common.LINE_BREAK[:2])
                    f.write(time.accept(visitor))
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Time resolution services API */"
                        + Common.LINE_BREAK[:2]
                    )
                    f.write(time.accept(visitor, resolution=True))

                if self._language == "c++":
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// All the operations for this Container interface will be declared as\n"
                        + Common.SPACE_INDENTATION[:5]
                        + "// public concrete methods here in the order that the container operations\n"
                        + Common.SPACE_INDENTATION[:5]
                        + "// are defined in the XML"
                        + Common.LINE_BREAK[:2]
                    )
                    f.write(Common.SPACE_INDENTATION[:5] + "// The following describes the APIs generated:\n")
                    f.write(Common.SPACE_INDENTATION[:5] + "// * For any Event: send\n")
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Synchronous Request-Response: request_sync operation\n"
                    )
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any Asynchronous Request-Response: request_async operation\n"
                    )
                    f.write(Common.SPACE_INDENTATION[:5] + "// * For any Request-Response: response operation\n")
                    f.write(
                        Common.SPACE_INDENTATION[:5] + "// * For any Versioned Data Read Access: get_read_access,\n"
                    )
                    f.write(Common.SPACE_INDENTATION[:5] + "// release_read_access\n")
                    f.write(
                        Common.SPACE_INDENTATION[:5] + "// * For any Versioned Data Write Access: get_write_access,\n"
                    )
                    f.write(Common.SPACE_INDENTATION[:5] + "// cancel_write_access, publish_write_access\n")
                    f.write(Common.SPACE_INDENTATION[:5] + "// * For any Get_Properties: get_#property_name#_value\n")
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// * For any PINFO Read Access: read, seek"
                        + Common.LINE_BREAK[:2]
                    )

                # Event functions prototypes
                events_send = self._ecoa_model.events_send.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if events_send:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Event operation call specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("EventSent"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for send in events_send:
                        f.write(send.accept(visitor))

                # Request-Response functions prototypes
                requests_send = self._ecoa_model.requests_send.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                requests_received = self._ecoa_model.requests_received.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if requests_send or requests_received:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Request-response call specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("ResquestResponse"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for send in requests_send:
                        f.write(send.accept(visitor))
                    for received in requests_received:
                        f.write(received.accept(visitor))

                # Versioned Data functions prototypes
                data_read = self._ecoa_model.data_read.get(self._component_impl_name + ":" + self._module_impl_name, [])
                data_written = self._ecoa_model.data_written.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if data_read or data_written:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Versioned data call specifications */"
                        + Common.LINE_BREAK[:1]
                    )
                    f.write(Common.SPACE_INDENTATION[:indent_level] + "/* ")
                    for comment in self._service_comment_helper.find_all("Data"):
                        f.write(" " + comment + " ")
                    f.write(" */" + Common.LINE_BREAK[:2])
                    for read in data_read:
                        f.write(read.accept(visitor))
                    for written in data_written:
                        f.write(written.accept(visitor))

                # Get Value functions prototype
                properties = self._ecoa_model.properties.get(
                    self._component_impl_name + ":" + self._module_impl_name, []
                )
                if properties:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Functional parameters call specifications */"
                        + Common.LINE_BREAK[:2]
                    )
                    for property in properties:
                        f.write(property.accept(visitor))

                # PINFO functions prototypes
                pinfos = self._ecoa_model.pinfos.get(self._component_impl_name + ":" + self._module_impl_name, [])
                if pinfos:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Persistent Information management operations */"
                        + Common.LINE_BREAK[:2]
                    )
                    for pinfo in pinfos:
                        f.write(pinfo.accept(visitor))

                # Recovery Action
                if module_type.is_fault_handler:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Recovery action service API call specification */"
                        + Common.LINE_BREAK[:2]
                    )
                    f.write(generator.recovery_action.generate((self._module_impl_name, self._language)))

                # Save Warm Start Context
                if module_type.has_warm_start_context:
                    f.write(
                        Common.SPACE_INDENTATION[:indent_level]
                        + "/* Optional API for saving the warm start context */"
                        + Common.LINE_BREAK[:2]
                    )
                    f.write(generator.save_warm_start_context.generate((self._module_impl_name, self._language)))

                if self._language == "c":
                    f.write(
                        "/* Context management operation */"
                        + Common.LINE_BREAK[:2]
                        + "void\n"
                        + self._module_impl_name
                        + "_container__save_non_volatile_context(\n"
                        + Common.SPACE_INDENTATION[:2]
                        + self._module_impl_name
                        + "__context* context\n);"
                        + Common.LINE_BREAK[:2]
                        + "void\n"
                        + self._module_impl_name
                        + "_release_all_data_handles(\n"
                        + Common.SPACE_INDENTATION[:2]
                        + self._module_impl_name
                        + "__context* context\n);"
                        + Common.LINE_BREAK[:2]
                    )
                elif self._language == "c++":
                    f.write(
                        Common.SPACE_INDENTATION[:5]
                        + "// Other container technical data will accessible through the incomplete"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[:5]
                        + "// structure defined here:"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[:5]
                        + "struct platform_hook;"
                        + Common.LINE_BREAK[:2]
                        + Common.SPACE_INDENTATION[:5]
                        + "// The constructor of the Container shall have the following signature:\n"
                        + Common.SPACE_INDENTATION[:5]
                        + "Container(platform_hook* hook);"
                        + Common.LINE_BREAK[:2]
                        + Common.SPACE_INDENTATION[:2]
                        + "private:"
                        + Common.LINE_BREAK[:2]
                        + Common.SPACE_INDENTATION[:5]
                        + "// private data for this container implementation is declared as a\n"
                        + Common.SPACE_INDENTATION[:5]
                        + "// private struct within the implementation\n"
                        + Common.SPACE_INDENTATION[:5]
                        + "platform_hook *hook;\n"
                        + "}; /* Container */"
                        + Common.LINE_BREAK[:2]
                        + Common.generate_close_namespace(self._module_impl_name)
                    )
                f.write(Common.generate_header_close_guard(self._module_impl_name, self._language, file_type))
                logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
