# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""TypesGenerator class."""

# Standard library imports
import logging
import os
from typing import Any, List

import pkg_resources

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.types.derived.array import ArrayGenerator
from ecoa_toolset.generators.types.derived.constant import ConstantGenerator
from ecoa_toolset.generators.types.derived.enum import EnumGenerator
from ecoa_toolset.generators.types.derived.record import RecordGenerator
from ecoa_toolset.generators.types.derived.simple import SimpleGenerator
from ecoa_toolset.generators.types.derived.variant_record import VariantRecordGenerator
from ecoa_toolset.generators.types.sorter import TypesSorter
from ecoa_toolset.models.ecoa_objects import ecoa_common_2_0, ecoa_types_2_0

logger = logging.getLogger(__name__)


class TypesGenerator:
    """The Types Generator.

    Args:
        ecoa_model : The ECOA model.
        path (str) : The generation directory path.
        force (bool) : True if the files can be overwritten, false otherwise.
        templates : The Templates.
    """

    def __init__(self, ecoa_model, path: str, force: bool, templates=None):
        self._ecoa_model = ecoa_model
        self._path = os.path.join(path, "0-Types/inc")
        self._force = force
        self._templates = templates
        self._indent_level = 0
        self._indent_step = 2

    def _generate_header_template(self, library_name: str, language: str) -> str:
        generation = "/*\n"
        generation += f" * @file {library_name.replace('.', '__')}.h{Common.switch_lang('', 'pp', language)}\n"
        generation += " * Data-type declaration file\n"
        generation += " * Generated automatically from specification; do not modify here\n"
        generation += " */\n\n"
        return generation

    def _generate_includes(self, use: List[ecoa_common_2_0.Use], language: str) -> str:
        generation = ""
        for include in use:
            generation += f'#include "{include.library.replace(".", "__")}.h{Common.switch_lang("", "pp", language)}"'
            generation += Common.LINE_BREAK[:1]
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_complex_type(self, element: Any, library_name: str, language: str) -> str:
        generation = ""
        logger.debug(f"{Common.TAB_INDENTATION[:1]}Generating {type(element).__name__}: {element.name}")
        if isinstance(element, ecoa_types_2_0.Record):
            generation += RecordGenerator(
                element, library_name, language, self._indent_level, self._indent_step
            ).generate()
        elif isinstance(element, ecoa_types_2_0.VariantRecord):
            generation += VariantRecordGenerator(
                element, library_name, language, self._indent_level, self._indent_step
            ).generate()
        elif isinstance(element, ecoa_types_2_0.Array):
            generation += ArrayGenerator(
                element, library_name, language, self._indent_level, self._indent_step
            ).generate()
        elif isinstance(element, ecoa_types_2_0.FixedArray):
            generation += ArrayGenerator(
                element, library_name, language, self._indent_level, self._indent_step, fixed=True
            ).generate()
        elif isinstance(element, ecoa_types_2_0.Simple):
            generation += SimpleGenerator(
                element, library_name, language, self._indent_level, self._indent_step
            ).generate()
        elif isinstance(element, ecoa_types_2_0.Enum):
            generation += EnumGenerator(
                element, library_name, language, self._indent_level, self._indent_step, self._ecoa_model.types_helper
            ).generate()
        elif isinstance(element, ecoa_types_2_0.Constant):
            generation += ConstantGenerator(element, library_name, language, self._indent_level).generate()
        generation += Common.LINE_BREAK[:1]
        return generation

    def _generate_types(self, types: ecoa_types_2_0.DataTypes, library_name: str, language: str) -> str:
        orderedTypes = TypesSorter(self._ecoa_model, library_name, types).sort()
        generation = ""
        for element in orderedTypes:
            generation += self._generate_complex_type(element, library_name, language)
        return generation

    def _generate_custom_library(
        self,
        language: str,
        ext: str,
        library_name: str,
        use: List[ecoa_common_2_0.Use],
        types: ecoa_types_2_0.DataTypes,
    ) -> None:
        generation = ""
        if self._templates:
            generation += self._templates.generate(
                ext,
                library_name + ext,
                "Header for library " + library_name,
            )
        else:
            generation += self._generate_header_template(library_name, language)
        generation += Common.generate_header_open_guard(library_name, language)
        if language == "c++":
            generation += (
                "#if defined(__cplusplus)"
                + Common.LINE_BREAK[:1]
                + 'extern "C" {'
                + Common.LINE_BREAK[:1]
                + "#endif /* __cplusplus */"
                + Common.LINE_BREAK[:2]
            )
        generation += '#include "ECOA' + ext + '"' + Common.LINE_BREAK[:2]
        generation += self._generate_includes(use, language)
        namespaces = library_name.split("__")
        if language == "c++":
            for namespace in namespaces:
                generation += Common.SPACE_INDENTATION[: self._indent_level]
                generation += Common.generate_open_namespace(namespace)
                self._indent_level += self._indent_step
        generation += self._generate_types(types, library_name, language)
        if language == "c++":
            for namespace in namespaces:
                generation += Common.SPACE_INDENTATION[: (self._indent_level - self._indent_step)]
                generation += Common.generate_close_namespace(namespace)
                self._indent_level -= self._indent_step
            generation += (
                "#if defined(__cplusplus)"
                + Common.LINE_BREAK[:1]
                + "}"
                + Common.LINE_BREAK[:1]
                + "#endif /* __cplusplus */"
                + Common.LINE_BREAK[:2]
            )
        generation += Common.generate_header_close_guard(library_name, language)
        return generation

    def _generate_custom_librairies(self, language: str, ext: str) -> None:
        for library_name, library in self._ecoa_model.ecoa_xml_model._types.items():
            library_name = os.path.basename(library_name).split(".")[0]
            generation = self._generate_custom_library(language, ext, library_name, library.use, library.types)
            file_name = library_name + ext
            file_path = os.path.join(self._path, file_name)
            try:
                logger.info(f"Generating {file_path}")
                with open(file_path, "x") as f:
                    f.write(generation)
                logger.info(f"{file_path} generated")
            except FileExistsError:
                logger.warning(f"{file_path} already exists")

    def _generate_ecoa_library(self, language: str, ext: str) -> None:
        file_name = "ECOA" + ext
        generation = pkg_resources.resource_string(__name__, "./basic/" + file_name).decode("utf-8")
        generation = generation.replace("\r\n", "\n").replace("\r", "\n")
        file_path = os.path.join(self._path, file_name)
        try:
            logger.info(f"Generating {file_path}")
            with open(file_path, "x") as f:
                f.write(generation)
            logger.info(f"{file_path} generated")
        except FileExistsError:
            logger.warning(f"{file_path} already exists")

    def generate(self) -> None:
        """Generates the following files:
        .
        └── <output>
            └── 0-Types
                └── inc
                    └── ECOA.h
                    └── ECOA.hpp
                    └── namespace1.h
                    └── namespace1_namespace2.hpp
        """
        Common.create_sub_directory(self._path, self._force, ignored=True)
        for language in ["c", "c++"]:
            ext = ".h" + Common.switch_lang("", "pp", language)
            self._generate_ecoa_library(language, ext)
            self._generate_custom_librairies(language, ext)
