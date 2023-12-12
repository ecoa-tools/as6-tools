# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module User generation class.
"""

# Standard library imports
import logging
import os

# Internal library imports
from ecoa_toolset.generators.common import Common

# Local imports
from mscigt.templates import Templates

logger = logging.getLogger(__name__)


class ModuleUserGenerator:
    """"""

    _path: str = None
    _module_impl_name: str = None
    _language: str = None
    _templates: Templates = None

    def __init__(self, path: str, module_impl_name: str, language: str, templates: Templates) -> None:
        self._path = path
        self._module_impl_name = module_impl_name
        self._language = language
        self._templates = templates

    def generate(self) -> None:
        """Writes the module user context header code."""
        ext = ".h" + Common.switch_lang("", "pp", self._language)
        file_type = "user_context"
        file_name = self._module_impl_name + "_" + file_type + ext
        file_path = os.path.join(self._path, "inc", file_name)
        try:
            with open(file_path, "x") as f:
                f.write(
                    self._templates.generate(
                        ext,
                        file_name,
                        file_type.replace("_", " ").title() + " header for Module " + self._module_impl_name,
                    )
                )
                f.write(Common.generate_header_open_guard(self._module_impl_name, self._language, file_type))

                # Includes
                f.write("/* Standard Types */" + Common.LINE_BREAK[:1])
                f.write("#include <ECOA" + ext + ">" + Common.LINE_BREAK[:1])
                f.write("/* Additionally created types */" + Common.LINE_BREAK[:1])
                f.write("/* Container Types */" + Common.LINE_BREAK[:1])
                f.write('#include "' + self._module_impl_name + "_container_types" + ext + '"' + Common.LINE_BREAK[:2])
                if self._language == "c++":
                    f.write(Common.generate_open_namespace(self._module_impl_name))
                #  User Module Context structure
                f.write(
                    "/* User Module Context structure example */"
                    + Common.LINE_BREAK[:1]
                    + "typedef struct"
                    + Common.LINE_BREAK[:1]
                    + "{"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:4]
                    + '/* declare the User Module Context "local" data here */'
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:4]
                    + "ECOA"
                    + Common.switch_lang("__", "::", self._language)
                    + "uint32 unused;"
                    + Common.LINE_BREAK[:1]
                    + "}"
                    + Common.SPACE_INDENTATION[:3]
                    + Common.switch_lang(self._module_impl_name + "_", "", self._language)
                    + "user_context;"
                    + Common.LINE_BREAK[:2]
                )
                #  Warm Start Module Context structure
                f.write(
                    "/* Warm Start Module Context structure example */"
                    + Common.LINE_BREAK[:1]
                    + "typedef struct"
                    + Common.LINE_BREAK[:1]
                    + "{"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:4]
                    + "/* declare the Warm Start Module Context data here */"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[:4]
                    + "ECOA"
                    + Common.switch_lang("__", "::", self._language)
                    + "uint32 unused;"
                    + Common.LINE_BREAK[:1]
                    + "}"
                    + Common.SPACE_INDENTATION[:3]
                    + Common.switch_lang(self._module_impl_name + "_", "", self._language)
                    + "warm_start_context;"
                    + Common.LINE_BREAK[:2]
                )
                if self._language == "c++":
                    f.write(Common.generate_close_namespace(self._module_impl_name))
                f.write(Common.generate_header_close_guard(self._module_impl_name, self._language, file_type))
                logger.debug("%s generated", file_path)
        except FileExistsError:
            logger.warning("%s already exists", file_path)
