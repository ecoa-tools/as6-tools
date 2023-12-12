# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Container visitor class.
"""

# Standard library imports
from typing import List

# Internal library imports
from ecoa_toolset.models.components import (
    DataRead,
    DataWritten,
    EventSend,
    External,
    Log,
    Pinfo,
    Property,
    RequestReceived,
    RequestSend,
    Time,
)
from ecoa_toolset.models.visitor import Visitor


class ContainerVisitor(Visitor):
    """The Container Visitor."""

    _generator = None
    _event_send_generated: List[str] = None
    _request_send_generated: List[str] = None
    _response_send_generated: List[str] = None
    _data_read_generated: List[str] = None
    _data_written_generated: List[str] = None

    def __init__(self, generator):
        self._generator = generator
        self._event_send_generated = []
        self._request_send_generated = []
        self._response_send_generated = []
        self._data_read_generated = []
        self._data_written_generated = []

    def visit_data_read(self, element: DataRead) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._data_read_generated:
            self._data_read_generated.append(key)
            generation += self._generator.versioned_data.generate(element, "read")
        return generation

    def visit_data_written(self, element: DataWritten) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._data_written_generated:
            self._data_written_generated.append(key)
            generation += self._generator.versioned_data.generate(element, "write")
        return generation

    def visit_event_send(self, element: EventSend) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._event_send_generated:
            self._event_send_generated.append(key)
            generation += self._generator.event_send.generate(element)
        return generation

    def visit_external(self, element: External, **kwargs) -> str:
        generation = self._generator.external.generate(element)
        return generation

    def visit_log(self, element: Log, **kwargs) -> str:
        generation = self._generator.logs.generate(element)
        return generation

    def visit_pinfo(self, element: Pinfo, **kwargs) -> str:
        generation = self._generator.pinfo.read.generate(element)
        generation += self._generator.pinfo.seek.generate(element)
        return generation

    def visit_property(self, element: Property, **kwargs) -> str:
        generation = self._generator.get_value.generate(element)
        return generation

    def visit_request_received(self, element: RequestReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._response_send_generated:
            self._response_send_generated.append(key)
            generation += self._generator.response_send.generate(element)
        return generation

    def visit_request_send(self, element: RequestSend) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._request_send_generated:
            self._request_send_generated.append(key)
            generation += self._generator.request_send.generate(element)
        return generation

    def visit_time(self, element: Time, **kwargs) -> str:
        generation = ""
        if kwargs.get("resolution") is True:
            generation += (
                self._generator.time.relative_local_time_resolution.generate(element)
                + self._generator.time.utc_time_resolution.generate(element)
                + self._generator.time.absolute_system_time_resolution.generate(element)
            )
        else:
            generation += (
                self._generator.time.relative_local_time.generate(element)
                + self._generator.time.utc_time.generate(element)
                + self._generator.time.absolute_system_time.generate(element)
            )
        return generation
