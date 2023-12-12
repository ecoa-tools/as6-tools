# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""DataParser class.
"""

from typing import Dict

# Internal library imports
from ecoa_toolset.models.components import DataRead, DataWritten, Link


class DataParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None
    _links: Dict[str, Dict] = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name
        self._links = {"readers": {}, "writers": {}}

    def _build_links(self, readers, writers, controlled: bool) -> None:
        reader_links = [
            Link(
                reader_type,
                reader.instance_name,
                reader.operation_name,
                getattr(reader, "activating", True),
                None,
                controlled=controlled,
            )
            for reader_type, readers_list in readers.items()
            for reader in readers_list or []
        ]
        writer_links = [
            Link(
                writer_type,
                writer.instance_name,
                writer.operation_name,
                None,
                None,
                controlled=controlled,
            )
            for writer_type, writers_list in writers.items()
            for writer in writers_list or []
        ]
        for reader_link in reader_links:
            self._links["readers"][reader_link] = writer_links
        for writer_link in writer_links:
            self._links["writers"][writer_link] = reader_links

    def _build_all_links(self) -> None:
        for link in self._component_implementation.data_link:
            if getattr(link, "readers", "") and getattr(link, "writers", ""):
                readers = {k: v for k, v in link.readers.__dict__.items() if v is not None}
                writers = {k: v for k, v in link.writers.__dict__.items() if v is not None}
                self._build_links(readers, writers, link.controlled)

    def _build_data_read(self, module_type, module_impl, module_inst_names, data_read) -> None:
        data = DataRead(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            data_read.name,
            self._ecoa_model.types_helper.add_namespace(data_read.type),
            data_read.max_versions,
            data_read.notifying,
            {
                key: value
                for key, value in self._links["readers"].items()
                if key.type == "module_instance"
                and key.instance_name in module_inst_names
                and key.operation_name == data_read.name
            },
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.data_read:
            self._ecoa_model.data_read[key].append(data)
        else:
            self._ecoa_model.data_read[key] = [data]

    def _build_data_written(self, module_type, module_impl, module_inst_names, data_written) -> None:
        dico_write = {
            key: value
            for key, value in self._links["writers"].items()
            if key.type == "module_instance"
            and key.instance_name in module_inst_names
            and key.operation_name == data_written.name
        }
        dico_key = {}
        for key, value in dico_write.items():
            list_key = []
            for key2, value2 in self._links["writers"].items():
                if key != key2 and value == value2 and key.instance_name == key2.instance_name:
                    list_key.append(key2)
            dico_key[key] = list_key
        data = DataWritten(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            data_written.name,
            self._ecoa_model.types_helper.add_namespace(data_written.type),
            data_written.max_versions,
            data_written.write_only,
            dico_write,
            dico_key,
        )

        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.data_written:
            self._ecoa_model.data_written[key].append(data)
        else:
            self._ecoa_model.data_written[key] = [data]

    def _build_data(self) -> None:
        for module_impl in self._component_implementation.module_implementation:
            module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
            module_inst_names = [
                module_inst.name
                for module_inst in self._component_implementation.module_instance
                if module_inst.implementation_name == module_impl.name
            ]
            for data_read in module_type.operations.data_read:
                self._build_data_read(module_type, module_impl, module_inst_names, data_read)
            for data_written in module_type.operations.data_written:
                self._build_data_written(module_type, module_impl, module_inst_names, data_written)

    def compute(self) -> None:
        if not (self._links.get("readers") and self._links.get("writers")):
            self._build_all_links()
        self._build_data()
