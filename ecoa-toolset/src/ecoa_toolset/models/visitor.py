# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Class to visit ECOA components.
"""

# Standard library imports
from typing import Any

# Internal library imports
from ecoa_toolset.models.components import (
    DataRead,
    DataWritten,
    EventReceived,
    EventSend,
    External,
    Log,
    Parameter,
    Pinfo,
    Property,
    RequestReceived,
    RequestSend,
    Time,
)


class Visitor:
    """The base class for all visitor class that wants ECOA components data."""

    def visit_log(self, element: Log, **kwargs) -> Any:
        pass

    def visit_time(self, element: Time, **kwargs) -> Any:
        pass

    def visit_parameter(self, element: Parameter, **kwargs) -> Any:
        pass

    def visit_event_send(self, element: EventSend, **kwargs) -> Any:
        pass

    def visit_request_send(self, element: RequestSend, **kwargs) -> Any:
        pass

    def visit_event_received(self, element: EventReceived, **kwargs) -> Any:
        pass

    def visit_request_received(self, element: RequestReceived, **kwargs) -> Any:
        pass

    def visit_data_read(self, element: DataRead, **kwargs) -> Any:
        pass

    def visit_data_written(self, element: DataWritten, **kwargs) -> Any:
        pass

    def visit_property(self, element: Property, **kwargs) -> Any:
        pass

    def visit_pinfo(self, element: Pinfo, **kwargs) -> Any:
        pass

    def visit_external(self, element: External, **kwargs) -> Any:
        pass
