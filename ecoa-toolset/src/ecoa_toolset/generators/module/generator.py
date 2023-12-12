# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Module functions generation class.
"""

# Internal library imports
from ecoa_toolset.generators.module.functions.data_updated import DataUpdatedGenerator
from ecoa_toolset.generators.module.functions.error_notification import ErrorNotificationGenerator
from ecoa_toolset.generators.module.functions.event_received import EventReceivedGenerator
from ecoa_toolset.generators.module.functions.request_received import RequestReceivedGenerator
from ecoa_toolset.generators.module.functions.response_received import ResponseReceivedGenerator


class ModuleGenerator:
    """The Module Generator."""

    event_received: EventReceivedGenerator = None
    error_notification: ErrorNotificationGenerator = None
    request_received: RequestReceivedGenerator = None
    response_received: ResponseReceivedGenerator = None
    data_updated: DataUpdatedGenerator = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        self.event_received = EventReceivedGenerator(indent_level, indent_step, body)
        self.error_notification = ErrorNotificationGenerator(indent_level, indent_step, body)
        self.request_received = RequestReceivedGenerator(indent_level, indent_step, body)
        self.response_received = ResponseReceivedGenerator(indent_level, indent_step, body)
        self.data_updated = DataUpdatedGenerator(indent_level, indent_step, body)
