# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Container Types generation class.
"""

# Standard library imports
import logging
import os

# Local imports
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.generators.common import Common

logger = logging.getLogger(__name__)


class ContainerTypesGenerator:
    """"""

    _ecoa_model = None
    _path: str = None
    _component_impl_name: str = None
    _module_impl_name: str = None
    _language: str = None
    _templates: Templates = None

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

    def _generate_versioned_data_handles(self) -> str:
        """Generates the container types header versioned data handle structure code."""
        generation = ""
        data_written = self._ecoa_model.data_written.get(self._component_impl_name + ":" + self._module_impl_name, [])
        data_read = self._ecoa_model.data_read.get(self._component_impl_name + ":" + self._module_impl_name, [])
        for data in data_written + data_read:
            generation += (
                "/*\n"
                + " * The following is the data handle structure associated to the data operation\n"
                + " * called "
                + data.name
                + " of data-type "
                + data.type
                + "\n"
                + " */\n"
                + "typedef struct {\n"
                + Common.SPACE_INDENTATION[:3]
                + "/* pointer to the local copy of the data */\n"
                + Common.SPACE_INDENTATION[:3]
                + data.type.replace(":", Common.switch_lang("__", "::", self._language)).replace(
                    ".", Common.switch_lang("__", "::", self._language)
                )
                + "* data;\n"
                + Common.SPACE_INDENTATION[:3]
                + "/* stamp updated each time the data value is updated locally for that */\n"
                + Common.SPACE_INDENTATION[:3]
                + "/* reader */\n"
                + Common.SPACE_INDENTATION[:3]
                + "ECOA"
                + Common.switch_lang("__", "::", self._language)
                + "uint32 stamp;\n"
                + Common.SPACE_INDENTATION[:3]
                + "/* technical info associated with the data (opaque for the user, reserved */\n"
                + Common.SPACE_INDENTATION[:3]
                + "/* for the infrastructure) */\n"
                + Common.SPACE_INDENTATION[:3]
                + "ECOA"
                + Common.switch_lang("__", "::", self._language)
                + "byte platform_hook[ECOA_VERSIONED_DATA_HANDLE_PRIVATE_SIZE];\n"
                + "} "
            )
            if self._language == "c":
                generation += self._module_impl_name + "_container__"
            generation += data.name + "_handle;" + Common.LINE_BREAK[:2]
        return generation

    def generate(self) -> None:
        """Generates the container types header code."""
        ext = ".h" + Common.switch_lang("", "pp", self._language)
        file_type = "container_types"
        file_name = self._module_impl_name + "_" + file_type + ext
        file_path = os.path.join(self._path, "inc-gen", file_name)
        try:
            with open(file_path, "x") as f:
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        file_type.replace("_", " ").title() + " header for Module " + self._module_impl_name,
                        file_unmodifiable=True,
                    )
                )
                f.write(Common.generate_header_open_guard(self._module_impl_name, self._language, file_type))
                f.write(Common.generate_includes(self._ecoa_model.use[self._component_impl_name], self._language))
                f.write(
                    "#include <ECOA.h"
                    + ("pp" if self._language == "c++" else "")
                    + ">"
                    + Common.LINE_BREAK[:2]
                    + "#define ECOA_VERSIONED_DATA_HANDLE_PRIVATE_SIZE 32"
                    + Common.LINE_BREAK[:2]
                )
                if self._language == "c++":
                    f.write(Common.generate_open_namespace(self._module_impl_name))
                f.write(
                    "/* The following describes the data types generated with regard to APIs:"
                    + Common.LINE_BREAK[:1]
                    + " * For any Versioned Data Read Access: data_handle"
                    + Common.LINE_BREAK[:1]
                    + " * For any Versioned Data Write Access: data_handle"
                    + Common.LINE_BREAK[:1]
                    + " */"
                    + Common.LINE_BREAK[:2]
                )
                f.write(self._generate_versioned_data_handles())
                if self._language == "c++":
                    f.write(Common.generate_close_namespace(self._module_impl_name))
                f.write(Common.generate_header_close_guard(self._module_impl_name, self._language, file_type))
                logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
