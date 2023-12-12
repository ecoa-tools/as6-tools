# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module visitor class.
"""

# Standard library imports
from typing import List

# Internal library imports
from ecoa_toolset.models.components import DataRead, EventReceived, RequestReceived, RequestSend
from ecoa_toolset.models.visitor import Visitor


class ModuleVisitor(Visitor):
    """The Module Visitor."""

    _generator = None
    _data_updated_generated: List[str] = None
    _event_received_generated: List[str] = None
    _request_received_generated: List[str] = None
    _response_received_generated: List[str] = None

    def __init__(self, generator):
        self._generator = generator
        self._data_updated_generated = []
        self._event_received_generated = []
        self._request_received_generated = []
        self._response_received_generated = []

    def visit_data_read(self, element: DataRead) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._data_updated_generated:
            self._data_updated_generated.append(key)
            generation += self._generator.data_updated.generate(element)
        return generation

    def visit_event_received(self, element: EventReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._event_received_generated:
            self._event_received_generated.append(key)
            generation += self._generator.event_received.generate(element)
        return generation

    def visit_request_received(self, element: RequestReceived) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._request_received_generated:
            self._request_received_generated.append(key)
            generation += self._generator.request_received.generate(element)
        return generation

    def visit_request_send(self, element: RequestSend) -> str:
        generation = ""
        key = f"{element.component_impl_name}:{element.module_impl_name}:{element.name}"
        if key not in self._response_received_generated:
            self._response_received_generated.append(key)
            generation += self._generator.response_received.generate(element)
        return generation
