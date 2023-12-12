# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Common attributes for code generation.
"""

# Standard library imports
import logging
import os
import shutil
from typing import Any, ClassVar, List, Set

# Internal library imports
from ecoa_toolset.models.components import Variable

logger = logging.getLogger(__name__)


class Common:
    """Common attributes."""

    LINE_BREAK: ClassVar[str] = 20 * "\n"
    SPACE_INDENTATION: ClassVar[str] = 20 * " "
    TAB_INDENTATION: ClassVar[str] = 20 * "\t"

    @classmethod
    def switch_lang(cls, element_c: Any, element_cpp: Any, lang: str) -> Any:
        """Switch between the first two entries depending on the specified language (c or c++).

        Args:
            element_c (Any) : The C element.
            element_cpp (Any) : The C++ element.
            lang (str) : The language.

        Return:
            Any : The element in the selected language.

        """
        return element_c if lang == "c" else (element_cpp if lang == "c++" else None)

    @classmethod
    def construct_complete_variable_type(
        cls, element: Variable, lang: str, is_parameter: bool = False, out: bool = False
    ) -> str:
        result = ""
        if is_parameter and out is False:
            result += "const "
        result += (
            element.namespace.replace(".", cls.switch_lang("__", "::", lang))
            + cls.switch_lang("__", "::", lang)
            + element.type
        )
        if is_parameter and (out or getattr(element.type_category, "is_complex", "")):
            result += cls.SPACE_INDENTATION[:1] + cls.switch_lang("*", "&", lang)
        return result

    @classmethod
    def generate_function_parameters(
        cls, parameters: List, language: str, indent_level: int, is_out: bool = False, last_comma: bool = False
    ) -> str:
        generation = ""
        for index, parameter in enumerate(parameters or []):
            generation += (
                cls.SPACE_INDENTATION[:indent_level]
                + cls.construct_complete_variable_type(parameter, language, is_parameter=True, out=is_out)
                + cls.SPACE_INDENTATION[:1]
                + parameter.name
                + ("" if not last_comma and index == len(parameters) - 1 else ",")
                + cls.LINE_BREAK[:1]
            )
        return generation

    @classmethod
    def cast_unused_parameters(cls, parameters: List, parameters_used: Set, indent_level: int) -> str:
        generation = ""
        for parameter in parameters or []:
            if parameter.namespace + ":" + parameter.type + ":" + parameter.name not in parameters_used:
                generation += (
                    cls.SPACE_INDENTATION[:indent_level] + "(void) " + parameter.name + ";" + cls.LINE_BREAK[:1]
                )
        return generation

    @classmethod
    def generate_includes(cls, libraries: List[str], language: str) -> str:
        generation = ""
        for library in libraries:
            generation += (
                f'#include "{library.replace(".", "__")}.h{cls.switch_lang("", "pp", language)}"{cls.LINE_BREAK[:1]}'
            )
        generation += cls.LINE_BREAK[:1]
        return generation

    @classmethod
    def generate_header_open_guard(cls, module_impl_name: str, language: str, file_type: str = None) -> str:
        """Generates the opening header guard code.

        Args:
            module_impl_name (str) : The module implementation name.
            language (str) : The module implementation language.
            file_type (str) : The file type (Optional).

        Return:
            str : The opening header guard code.
        """
        generation = "#if !defined(" + module_impl_name.upper()
        if file_type:
            generation += "_" + file_type.upper()
        generation += (
            "_H"
            + ("PP" if language == "c++" else "")
            + ")"
            + cls.LINE_BREAK[:1]
            + "#define "
            + module_impl_name.upper()
        )
        if file_type:
            generation += "_" + file_type.upper()
        generation += "_H" + ("PP" if language == "c++" else "") + cls.LINE_BREAK[:2]
        if language == "c":
            generation += "#if defined(__cplusplus)" + cls.LINE_BREAK[:1]
            generation += 'extern "C" {' + cls.LINE_BREAK[:1]
            generation += "#endif /* __cplusplus */" + cls.LINE_BREAK[:2]
        return generation

    @classmethod
    def generate_header_close_guard(cls, module_impl_name: str, language: str, file_type: str = None) -> str:
        """Generates the closing header guard code.

        Args:
            module_impl_name (str) : The module implementation name.
            language (str) : The module implementation language.
            file_type (str) : The file type (Optional).

        Return:
            str : The closing header guard code
        """
        generation = ""
        if language == "c":
            generation += "#if defined(__cplusplus)" + cls.LINE_BREAK[:1]
            generation += "}" + cls.LINE_BREAK[:1]
            generation += "#endif  /* __cplusplus */" + cls.LINE_BREAK[:2]
        generation += "#endif /* " + module_impl_name.upper()
        if file_type:
            generation += "_" + file_type.upper()
        generation += "_H" + ("PP" if language == "c++" else "") + " */" + cls.LINE_BREAK[:1]
        return generation

    @classmethod
    def generate_open_namespace(cls, module_impl_name: str) -> str:
        """Generates the opening namespace code.

        Arg:
            module_impl_name (str) : The module implementation name.

        Return:
            str : The opening namespace code.
        """
        return "namespace " + module_impl_name + " {" + cls.LINE_BREAK[:2]

    @classmethod
    def generate_close_namespace(cls, module_impl_name: str, nb_line_break: int = 2) -> str:
        """Generates the closing namespace code.

        Args:
            module_impl_name (str) : The module implementation name.
            nb_line_break (int) : The number of line breaks.

        Return:
            str : The closing namespace code.
        """
        return "} /* " + module_impl_name + " */" + cls.LINE_BREAK[:nb_line_break]

    @classmethod
    def compute_relative_path(cls, src: str, dst: str) -> str:
        """Compute the relative path between two paths.

        Args:
            src (str) : The source path.
            dst (str) : The destination path.

        Returns:
            str : The relative path.
        """
        return os.path.relpath(os.path.abspath(dst), start=os.path.abspath(src))

    @classmethod
    def replace_escape_string(cls, path: str) -> str:
        return path.replace("\\", "\\\\")

    @classmethod
    def create_sub_directory(cls, path: str, force: bool, ignored: bool = False) -> None:
        """Create the path directory if not existing or overwrite it if force activate.

        Args:
            path (str) : Path to create or overwrite.
            force (bool) : True if the files can be overwritten, false otherwise.
        """
        logger.info("Attempt to create directory %s", path)
        if os.path.exists(path):
            if force:
                shutil.rmtree(path)
                logger.debug("%s already exists, forcing, overwriting it...", path)
            elif ignored:
                logger.debug("%s already exists.")
                return
            else:
                raise Exception("%s already exists ! Please use -f or --force flag to overwrite its contents." % path)
        os.makedirs(path)
        logger.debug("Created %s", path)
