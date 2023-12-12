# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Versioned Data generation class.
"""

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator
from ecoa_toolset.models.components import DataRead, DataWritten, VersionedData


class VersionedDataGenerator(FunctionGenerator):
    """"""

    type: str = None
    mode: str = None
    unit_test: bool = None

    def __init__(self, indent_level: int, indent_step: int, body: bool, unit_test: bool):
        super().__init__(indent_level, indent_step, body)
        self.unit_test = unit_test

    def _generate_prototype(self, element: VersionedData) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )

        generation += Common.switch_lang(
            element.module_impl_name + "_container__",
            element.module_impl_name + "::Container::" if self.body else "",
            element.language,
        )
        generation += element.name + "__" + self.mode + "_" + self.type + "_access (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level]
        if element.language == "c":
            generation += (
                element.module_impl_name
                + "__context * context,"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
            )
        generation += (
            Common.switch_lang(element.module_impl_name + "_container__", "", element.language)
            + element.name
            + "_handle "
            + Common.switch_lang("*", "&", element.language)
            + " data_handle"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_vd_instance_id(
        self, element: VersionedData, index: int, module_inst_name: str, component_name: str
    ) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + ("if" if index == 0 else "else if")
            + " ("
            + Common.switch_lang("context->platform_", "this->", element.language)
            + "hook->mod_id == "
            + module_inst_name.upper()
            + "_"
            + component_name.upper()
            + "_ID)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_vd_data_handle_storage(self, data_variable_name: str, language: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "data_handle"
            + Common.switch_lang("->", ".", language)
            + "data = "
            + data_variable_name
            + "_data;"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "data_handle"
            + Common.switch_lang("->", ".", language)
            + "stamp = "
            + data_variable_name
            + "_stamp;"
            + Common.LINE_BREAK[:1]
        )
        return generation

    def _generate_vd_return_status(self, language: str, else_statement: bool) -> str:
        generation = ""
        if else_statement:
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "else"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "{"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level += self.indent_step
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "return ECOA"
                + Common.switch_lang("__", "::", language)
                + "return_status"
                + Common.switch_lang("_", "::", language)
                + "INVALID_IDENTIFIER;"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        else:
            if language == "c":
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) data_handle;" + Common.LINE_BREAK[:2]
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.switch_lang("_OK", "()", language)
            + ";"
        )
        return generation

    def _generate_get_read_access_body(self, element: DataRead) -> str:
        generation = ""
        for index, (key_reader, (_, controlled)) in enumerate(element.writers.items()):
            module_inst_name_reader, component_name_reader, comp_op = tuple(key_reader.split(":"))
            generation += self._generate_vd_instance_id(element, index, module_inst_name_reader, component_name_reader)
            data_variable_name = (
                "CM_GLOBAL_" + module_inst_name_reader + "_" + component_name_reader + "__" + element.name
            )
            self.indent_level += self.indent_step
            if controlled:
                data_variable_name_copy = data_variable_name + "_copy"
                if element.language == "c++":
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "try"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "{"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level += self.indent_step
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + element.type.replace(":", Common.switch_lang("__", "::", element.language)).replace(
                        ".", Common.switch_lang("__", "::", element.language)
                    )
                    + " * "
                    + data_variable_name_copy
                    + " = "
                )
                generation += Common.switch_lang(
                    (
                        "("
                        + element.type.replace(":", "__").replace(".", "__")
                        + " *) malloc(sizeof("
                        + element.type.replace(":", "__")
                        + "));"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "if (!"
                        + data_variable_name_copy
                        + ")"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                        + "return ECOA__return_status_DATA_NOT_INITIALIZED;"
                        + Common.LINE_BREAK[:2]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                    ),
                    (
                        "new "
                        + element.type.replace(":", "::").replace(".", "::")
                        + ";"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "std::"
                    ),
                    element.language,
                )
                generation += (
                    "memcpy("
                    + data_variable_name_copy
                    + ", "
                    + data_variable_name
                    + "_data, sizeof("
                    + element.type.replace(":", Common.switch_lang("__", "::", element.language))
                    + "));"
                    + Common.LINE_BREAK[:2]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle"
                    + Common.switch_lang("->", ".", element.language)
                    + "data = "
                    + data_variable_name_copy
                    + ";"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle"
                    + Common.switch_lang("->", ".", element.language)
                    + "stamp = "
                    + data_variable_name
                    + "_stamp;"
                    + Common.LINE_BREAK[:1]
                )
                if element.language == "c++":
                    self.indent_level -= self.indent_step
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "}"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "catch (std::bad_alloc& e)"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "{"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level += self.indent_step
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "return ECOA::return_status(ECOA::return_status::EnumValues::OPERATION_NOT_AVAILABLE);"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level -= self.indent_step
                    generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
            else:
                generation += self._generate_vd_data_handle_storage(data_variable_name, element.language)
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
        generation += self._generate_vd_return_status(element.language, element.writers)
        return generation

    def _generate_get_write_access_body(self, element: DataWritten) -> str:
        generation = ""
        for index, (key_writer, (_, controlled)) in enumerate(element.readers.items()):
            module_inst_name_writer, component_name_writer, comp_op = tuple(key_writer.split(":"))
            generation += self._generate_vd_instance_id(element, index, module_inst_name_writer, component_name_writer)
            data_variable_name = (
                "CM_GLOBAL_" + module_inst_name_writer + "_" + component_name_writer + "__" + element.name
            )
            data_variable_name_first = (
                "CM_GLOBAL_"
                + module_inst_name_writer
                + "_"
                + component_name_writer
                + "__"
                + element.name
                + "_first_write"
            )
            data_variable_name_stamp = data_variable_name + "_stamp"
            self.indent_level += self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "if (" + data_variable_name_first
            for key, value in element.links_written.items():
                for write_link in value:
                    glob_other = (
                        "CM_GLOBAL_"
                        + write_link.instance_name
                        + "_"
                        + component_name_writer
                        + "__"
                        + write_link.operation_name
                        + "_first_write"
                    )
                    generation += " || " + glob_other
            generation += (
                ")"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "{"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level += self.indent_step
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + data_variable_name_first
                + " = 0;"
                + Common.LINE_BREAK[:1]
            )
            for key, value in element.links_written.items():
                for write_link in value:
                    glob_other = (
                        "CM_GLOBAL_"
                        + write_link.instance_name
                        + "_"
                        + component_name_writer
                        + "__"
                        + write_link.operation_name
                        + "_first_write"
                    )
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level] + glob_other + " = 0;" + Common.LINE_BREAK[:1]
                    )
            generation += Common.SPACE_INDENTATION[: self.indent_level]
            generation += Common.switch_lang(
                (
                    element.type.replace(":", "__").replace(".", "__")
                    + "* data = ("
                    + element.type.replace(":", "__").replace(".", "__")
                    + " *) malloc(sizeof("
                    + element.type.replace(":", "__").replace(".", "__")
                    + "));"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle->data = data;"
                ),
                (
                    element.type.replace(":", "::").replace(".", "::")
                    + "* data = new "
                    + element.type.replace(":", "::").replace(".", "::")
                    + ";"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle.data = data;"
                ),
                element.language,
            )
            generation += (
                Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "return ECOA"
                + Common.switch_lang("__", "::", element.language)
                + "return_status"
                + Common.switch_lang("_", "::", element.language)
                + "DATA_NOT_INITIALIZED;"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
            if controlled:
                data_variable_name_copy = data_variable_name + "_copy"
                if element.language == "c++":
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "try"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "{"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level += self.indent_step
                generation += (
                    Common.SPACE_INDENTATION[: self.indent_level]
                    + element.type.replace(":", Common.switch_lang("__", "::", element.language)).replace(
                        ".", Common.switch_lang("__", "::", element.language)
                    )
                    + " * "
                    + data_variable_name_copy
                    + " = "
                )
                generation += Common.switch_lang(
                    (
                        "("
                        + element.type.replace(":", "__").replace(".", "__")
                        + " *) malloc(sizeof("
                        + element.type.replace(":", "__")
                        + "));"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "if (!"
                        + data_variable_name_copy
                        + ")"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                        + "return ECOA__return_status_NO_DATA;"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                    ),
                    (
                        "new "
                        + element.type.replace(":", "::").replace(".", "::")
                        + ";"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                    ),
                    element.language,
                )
                generation += (
                    Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + data_variable_name_copy
                    + Common.SPACE_INDENTATION[1]
                    + "= "
                    + data_variable_name
                    + "_data;"
                    + Common.LINE_BREAK[:2]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle"
                    + Common.switch_lang("->", ".", element.language)
                    + "data ="
                    + Common.SPACE_INDENTATION[1]
                    + data_variable_name_copy
                    + ";"
                    + Common.LINE_BREAK[:1]
                    + Common.SPACE_INDENTATION[: self.indent_level]
                    + "data_handle"
                    + Common.switch_lang("->", ".", element.language)
                    + "stamp ="
                    + Common.SPACE_INDENTATION[1]
                    + data_variable_name_stamp
                    + ";"
                    + Common.LINE_BREAK[:1]
                )
                if element.language == "c++":
                    self.indent_level -= self.indent_step
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "}"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "catch (std::bad_alloc& e)"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + "{"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level += self.indent_step
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + "return ECOA::return_status(ECOA::return_status::EnumValues::OPERATION_NOT_AVAILABLE);"
                        + Common.LINE_BREAK[:1]
                    )
                    self.indent_level -= self.indent_step
                    generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
            else:
                generation += self._generate_vd_data_handle_storage(data_variable_name, element.language)
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
        generation += self._generate_vd_return_status(element.language, element.readers)
        return generation

    def _cast_argument(self, written_language, reader_language, reader_type) -> str:
        generation = ""
        if written_language == "c" and reader_language == "c++":
            generation += "(" + reader_type.replace(":", "::") + " *) "
        elif written_language == "c++" and reader_language == "c":
            generation += "(" + reader_type.replace(":", "__") + " *) "
        return generation

    def _generate_publish_write_access_body(self, element: DataWritten) -> str:
        generation = ""
        for index, (key_writer, (readers, notif)) in enumerate(element.readers.items()):
            module_inst_name_writer, component_name_writer, comp_op = tuple(key_writer.split(":"))
            generation += self._generate_vd_instance_id(element, index, module_inst_name_writer, component_name_writer)
            self.indent_level += self.indent_step
            written_global = "CM_GLOBAL_" + module_inst_name_writer + "_" + component_name_writer + "__" + element.name
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + written_global
                + "_data = data_handle"
                + Common.switch_lang("->", ".", element.language)
                + "data;"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + written_global
                + "_stamp += 1;"
                + Common.LINE_BREAK[:1]
            )
            for key, value in element.links_written.items():
                for write_link in value:
                    glob_other = (
                        "CM_GLOBAL_"
                        + write_link.instance_name
                        + "_"
                        + component_name_writer
                        + "__"
                        + write_link.operation_name
                    )
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + glob_other
                        + "_data = data_handle"
                        + Common.switch_lang("->", ".", element.language)
                        + "data;"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + glob_other
                        + "_stamp += 1;"
                        + Common.LINE_BREAK[:1]
                    )
            if not self.unit_test:
                generation += Common.LINE_BREAK[:1]
                for key_reader, reader in readers.items():
                    module_inst_name_reader, component_name_reader, comp_op_r = tuple(key_reader.split(":"))
                    data_variable_name = (
                        "CM_GLOBAL_" + module_inst_name_reader + "_" + component_name_reader + "__" + reader.name
                    )
                    generation += (
                        Common.SPACE_INDENTATION[: self.indent_level]
                        + data_variable_name
                        + "_data = "
                        + self._cast_argument(element.language, reader.language, reader.type)
                        + written_global
                        + "_data;"
                        + Common.LINE_BREAK[:1]
                        + Common.SPACE_INDENTATION[: self.indent_level]
                        + data_variable_name
                        + "_stamp"
                        + Common.SPACE_INDENTATION[1]
                        + "+= 1;"
                        + Common.LINE_BREAK[:1]
                    )
                generation += Common.LINE_BREAK[:1]
                for key_reader, reader in readers.items():
                    if reader.notifying:
                        module_inst_name_reader, component_name_reader, comp_op_r = tuple(key_reader.split(":"))
                        if reader.language == "c++":
                            generation += (
                                Common.SPACE_INDENTATION[: self.indent_level]
                                + module_inst_name_reader
                                + "_"
                                + component_name_reader
                                + "_Module."
                                + reader.name
                                + "__updated();"
                                + Common.LINE_BREAK[:1]
                            )
                        elif reader.language == "c":
                            generation += (
                                Common.SPACE_INDENTATION[: self.indent_level]
                                + reader.module_impl_name
                                + "__"
                                + reader.name
                                + "__updated(&"
                                + module_inst_name_reader
                                + "_"
                                + component_name_reader
                                + "_Context);"
                                + Common.LINE_BREAK[:1]
                            )
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:1]
        if element.readers:
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "else"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "{"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level += self.indent_step
            generation += (
                Common.SPACE_INDENTATION[: self.indent_level]
                + "return ECOA"
                + Common.switch_lang("__", "::", element.language)
                + "return_status"
                + Common.switch_lang("_", "::", element.language)
                + "INVALID_IDENTIFIER;"
                + Common.LINE_BREAK[:1]
            )
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        else:
            if element.language == "c":
                generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) data_handle;" + Common.LINE_BREAK[:2]
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )
        return generation

    def _generate_release_read_or_cancel_write_access_body(self, element: VersionedData) -> str:
        generation = Common.SPACE_INDENTATION[: self.indent_level]
        if element.language == "c":
            generation += (
                "(void) context;"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
                + "if (!data_handle)"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
                + "return ECOA__return_status_INVALID_HANDLE;"
                + Common.LINE_BREAK[:1]
                + Common.SPACE_INDENTATION[: self.indent_level]
            )
        generation += (
            "if (!data_handle"
            + Common.switch_lang("->", ".", element.language)
            + "data)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: (self.indent_level + self.indent_step)]
            + Common.switch_lang("free(data_handle->data);", "delete data_handle.data;", element.language)
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", element.language)
            + "return_status"
            + Common.switch_lang("_OK", "()", element.language)
            + ";"
        )
        return generation

    def _generate_body(self, element: VersionedData) -> str:
        generation = ""
        if self.mode == "get" and self.type == "read":
            generation += self._generate_get_read_access_body(element)
        elif self.mode == "get" and self.type == "write":
            generation += self._generate_get_write_access_body(element)
        elif self.mode == "publish" and self.type == "write":
            generation += self._generate_publish_write_access_body(element)
        elif self.mode == "release" or self.mode == "cancel":
            generation += self._generate_release_read_or_cancel_write_access_body(element)
        return generation

    def _generate_data_read(self, element: DataRead) -> str:
        generation = ""
        for mode in ["get", "release"]:
            self.mode = mode
            generation += super().generate(element)
        return generation

    def _generate_data_written(self, element: DataWritten) -> str:
        generation = ""
        for mode in ["get", "cancel", "publish"]:
            self.mode = mode
            generation += super().generate(element)
        return generation

    def generate(self, element: VersionedData, type: str) -> str:
        """"""
        self.type = type
        generation = ""
        if type == "read":
            generation += self._generate_data_read(element)
        elif type == "write":
            generation += self._generate_data_written(element)
        return generation
