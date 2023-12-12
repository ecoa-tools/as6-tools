# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""DataLinker class.
"""

from typing import List

# Internal library imports
from ecoa_toolset.models.components import DataRead, DataWritten, Link


class DataLinker:
    """"""

    _ecoa_model = None

    def __init__(self, ecoa_model):
        self._ecoa_model = ecoa_model

    def _link_read_and_written_with_module_instances(
        self,
        read: DataRead,
        read_reader_link: Link,
        read_writer_link: Link,
        written: DataWritten,
        written_writer_link: Link,
        written_reader_link: Link,
    ) -> None:
        if read.component_impl_name == written.component_impl_name:
            if read_reader_link == written_reader_link and written_writer_link == read_writer_link:
                read_component_names = self._ecoa_model.component_names.get(
                    read.component_impl_name + ":" + read_reader_link.instance_name, []
                )
                written_component_names = self._ecoa_model.component_names.get(
                    written.component_impl_name + ":" + written_writer_link.instance_name, []
                )
                for read_component_name in read_component_names:
                    for written_component_name in written_component_names:
                        key_reader = (
                            read_reader_link.instance_name
                            + ":"
                            + read_component_name
                            + ":"
                            + read_reader_link.operation_name
                        )
                        key_written = (
                            written_writer_link.instance_name
                            + ":"
                            + written_component_name
                            + ":"
                            + written_writer_link.operation_name
                        )
                        read.add_writer(key_reader, key_written, written)
                        written.add_reader(key_written, key_reader, read)

    def _link_read_and_written_with_services(
        self,
        read: DataRead,
        read_reader_link: Link,
        read_writer_link: Link,
        written: DataWritten,
        written_writer_link: Link,
        written_reader_link: Link,
    ) -> None:
        read_component_names = self._ecoa_model.component_names.get(
            read.component_impl_name + ":" + read_reader_link.instance_name
        )
        written_component_names = self._ecoa_model.component_names.get(
            written.component_impl_name + ":" + written_writer_link.instance_name
        )
        if not read_component_names or not written_component_names:
            return
        if read_writer_link.operation_name == written_reader_link.operation_name:
            for wire in self._ecoa_model.ecoa_xml_model._wires:
                key = None
                if (
                    wire.source.component_name in read_component_names
                    and wire.source.service_name == read_writer_link.instance_name
                    and wire.target.component_name in written_component_names
                    and wire.target.service_name == written_reader_link.instance_name
                ):
                    key = (
                        read_reader_link.instance_name
                        + ":"
                        + wire.source.component_name
                        + ":"
                        + read_reader_link.operation_name
                        + "::"
                        + written_writer_link.instance_name
                        + ":"
                        + wire.target.component_name
                        + ":"
                        + written_writer_link.operation_name
                    )
                elif (
                    wire.source.component_name in written_component_names
                    and wire.source.service_name == written_reader_link.instance_name
                    and wire.target.component_name in read_component_names
                    and wire.target.service_name == read_writer_link.instance_name
                ):
                    key = (
                        read_reader_link.instance_name
                        + ":"
                        + wire.target.component_name
                        + ":"
                        + read_reader_link.operation_name
                        + "::"
                        + written_writer_link.instance_name
                        + ":"
                        + wire.source.component_name
                        + ":"
                        + written_writer_link.operation_name
                    )
                if key:
                    key_reader, key_written = tuple(key.split("::"))
                    read.add_writer(key_reader, key_written, written)
                    written.add_reader(key_written, key_reader, read)

    def _compare_links(
        self,
        read: DataRead,
        read_reader_link: Link,
        read_writers_links: List[Link],
        written: DataWritten,
        written_writer_link: Link,
        written_readers_links: List[Link],
    ) -> None:
        for read_writer_link in read_writers_links:
            for written_reader_link in written_readers_links:
                if read_writer_link.type == "module_instance" and written_reader_link.type == "module_instance":
                    self._link_read_and_written_with_module_instances(
                        read,
                        read_reader_link,
                        read_writer_link,
                        written,
                        written_writer_link,
                        written_reader_link,
                    )
                elif read_writer_link.type == "reference" and written_reader_link.type == "service":
                    self._link_read_and_written_with_services(
                        read,
                        read_reader_link,
                        read_writer_link,
                        written,
                        written_writer_link,
                        written_reader_link,
                    )

    def _compare_data(self, read: DataRead, written: DataWritten):
        for read_reader_link, read_writers_links in read.links.items():
            for written_writer_link, written_readers_links in written.links.items():
                self._compare_links(
                    read, read_reader_link, read_writers_links, written, written_writer_link, written_readers_links
                )

    def compute(self) -> None:
        data_read = [read for v in self._ecoa_model.data_read.values() for read in v]
        data_written = [written for v in self._ecoa_model.data_written.values() for written in v]
        for read in data_read:
            for written in data_written:
                self._compare_data(read, written)
        for read in data_read:
            self._add_controlled_data_read(read)
        for written in data_written:
            self._add_controlled_data_written(written)

    def _add_controlled_data_read(self, read: DataRead) -> None:
        new_writers = {}
        controlled_dict = {}
        for link in read.links.keys():
            controlled_dict[link.instance_name] = link.controlled
        for key, value in read.writers.items():
            new_writers[key] = value, controlled_dict.get(key.split(":")[0])
        read.writers = new_writers

    def _add_controlled_data_written(self, written: DataWritten) -> None:
        new_readers = {}
        controlled_dict = {}
        for link in written.links.keys():
            controlled_dict[link.instance_name] = link.controlled
        for key, value in written.readers.items():
            new_readers[key] = value, controlled_dict.get(key.split(":")[0])
        written.readers = new_readers
