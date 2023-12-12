# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Representation of differents components of an ECOA project.
"""

# Standard library imports
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class Component(ABC):
    """The base class of all ECOA objects."""

    @abstractmethod
    def accept(self, visitor, **kwargs) -> None:
        pass


class Variable(Component):
    """The Variable.

    Args:
        name: Variable's name
        namespace: Variable's namespace
        type: Variable's type
        type_category: Variable's type_category
    """

    name: str = None
    namespace: str = None
    type: str = None
    type_category = None

    def __init__(self, name: str, namespace: str, type: str, type_category):
        self.name = name
        self.namespace = namespace
        self.type = type
        self.type_category = type_category

    def accept(self, visitor, **kwargs) -> Any:
        pass


class Parameter(Variable):
    """The Parameter.

    Args:
        name: Parameter's name
        type: Parameter's type
    """

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_parameter(self, **kwargs)


class Time(Component):
    """The Time Services.

    Args:
        component_impl_name: Component implementation name
        module_type_name: Module type name
        module_impl_name: Module implementation name
    """

    component_impl_name: str = None
    module_type_name: str = None
    module_impl_name: str = None
    language: str = None

    def __init__(self, component_impl_name: str, module_type_name: str, module_impl_name: str, language: str):
        self.component_impl_name = component_impl_name
        self.module_type_name = module_type_name
        self.module_impl_name = module_impl_name
        self.language = language

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_time(self, **kwargs)


class LogType(Enum):
    LOG_TRACE = 0
    LOG_DEBUG = 1
    LOG_INFO = 2
    LOG_WARNING = 3
    RAISE_ERROR = 4
    RAISE_FATAL_ERROR = 5


class Log(Component):
    """The Log.

    Args:
        component_impl_name: Component implementation name
        module_type_name: Module type name
        module_impl_name: Module implementation name
    """

    component_impl_name: str = None
    module_type_name: str = None
    module_impl_name: str = None
    language: str = None

    def __init__(self, component_impl_name: str, module_type_name: str, module_impl_name: str, language: str):
        self.component_impl_name = component_impl_name
        self.module_type_name = module_type_name
        self.module_impl_name = module_impl_name
        self.language = language

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_log(self, **kwargs)


class Link:
    """The Link."""

    type: str = None
    instance_name: str = None
    operation_name: str = None
    activating: bool = None
    language: str = None
    controlled: bool = None

    def __init__(
        self,
        type: str,
        instance_name: str,
        operation_name: str,
        activating: bool,
        language: str,
        controlled: bool = None,
    ):
        self.type = type
        self.instance_name = instance_name
        self.operation_name = operation_name
        self.activating = activating
        self.language = language
        self.controlled = controlled


class External(Component):
    """The External."""

    component_impl_name: str = None
    name: str = None
    inputs: List[Parameter] = None
    language: str = None
    links: Dict[Link, List[Link]] = None
    receivers: Dict = None

    def __init__(self, component_impl_name: str, name: str, language: str, links: Dict[Link, List[Link]]):
        self.component_impl_name = component_impl_name
        self.name = name
        self.language = language
        self.links = links
        self.receivers = {}

    def add_receiver(self, key_receiver: str, receiver: Any) -> None:
        self.receivers[key_receiver] = receiver

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_external(self, **kwargs)


class Trigger:
    """The Trigger."""

    component_impl_name: str = None
    name: str = None
    links: Dict[Link, List[Link]] = None
    receivers: Dict = None

    def __init__(self, component_impl_name: str, name: str, links: Dict[Link, List[Link]]):
        self.component_impl_name = component_impl_name
        self.name = name
        self.links = links
        self.receivers = {}

    def add_receiver(self, key_receiver: str, receiver: Any) -> None:
        self.receivers[key_receiver] = receiver


class DynamicTrigger:
    """The Dynamic Trigger."""

    component_impl_name: str = None
    name: str = None
    parameters: List[Parameter] = None
    links: Dict[Link, List[Link]] = None

    def __init__(self, component_impl_name: str, name: str, parameters: List[Parameter], links: Dict[Link, List[Link]]):
        self.component_impl_name = component_impl_name
        self.name = name
        self.parameters = parameters
        self.links = links


class DynamicTriggerSend(DynamicTrigger):
    """The Dynamic Trigger Send."""

    receivers: Dict = None

    def __init__(self, component_impl_name: str, name: str, parameters: List[Parameter], links: Dict[Link, List[Link]]):
        super().__init__(component_impl_name, name, parameters, links)
        self.receivers = {}

    def add_receiver(self, key_sender: str, key_receiver: str, receiver: Any) -> None:
        if self.receivers.get(key_sender):
            self.receivers[key_sender][key_receiver] = receiver
        else:
            self.receivers[key_sender] = {key_receiver: receiver}


class DynamicTriggerReceived(DynamicTrigger):
    """The Dynamic Trigger Received."""

    senders: Dict = None

    def __init__(self, component_impl_name: str, name: str, parameters: List[Parameter], links: Dict[Link, List[Link]]):
        super().__init__(component_impl_name, name, parameters, links)
        self.senders = {}

    def add_sender(self, key_receiver: str, key_sender: str, sender: Any) -> None:
        if self.senders.get(key_receiver):
            self.senders[key_receiver][key_sender] = sender
        else:
            self.senders[key_receiver] = {key_sender: sender}


class EventSend(Component):
    """The Event Send."""

    component_impl_name: str = None
    module_type_name: str = None
    module_impl_name: str = None
    language: str = None
    name: str = None
    inputs: List[Parameter] = None
    links: Dict[Link, List[Link]] = None
    receivers: Dict = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        inputs: List[Parameter],
        links: Dict[Link, List[Link]],
    ):
        self.component_impl_name = component_impl_name
        self.module_type_name = module_type_name
        self.module_impl_name = module_impl_name
        self.language = language
        self.name = name
        self.inputs = inputs
        self.links = links
        self.receivers = {}

    def add_receiver(self, key_sender: str, key_receiver: str, receiver: Any) -> None:
        if self.receivers.get(key_sender):
            self.receivers[key_sender][key_receiver] = receiver
        else:
            self.receivers[key_sender] = {key_receiver: receiver}

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_event_send(self, **kwargs)


class RequestSend(EventSend):
    """The Request Send."""

    is_synchronous: bool = None
    outputs: List[Parameter] = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        is_synchronous: bool,
        inputs: List[Parameter],
        outputs: List[Parameter],
        links: Dict[Link, List[Link]],
    ):
        super().__init__(component_impl_name, module_type_name, module_impl_name, language, name, inputs, links)
        self.is_synchronous = is_synchronous
        self.outputs = outputs

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_request_send(self, **kwargs)


class EventReceived(Component):
    """The Event Received."""

    component_impl_name: str = None
    module_type_name: str = None
    module_impl_name: str = None
    language: str = None
    name: str = None
    inputs: List[Parameter] = None
    links: Dict[Link, List[Link]] = None
    senders: Dict = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        inputs: List[Parameter],
        links: Dict[Link, List[Link]],
    ):
        self.component_impl_name = component_impl_name
        self.module_type_name = module_type_name
        self.module_impl_name = module_impl_name
        self.language = language
        self.name = name
        self.inputs = inputs
        self.links = links
        self.senders = {}

    def add_sender(self, key_receiver: str, key_sender: str, sender: Any) -> None:
        if self.senders.get(key_receiver):
            self.senders[key_receiver][key_sender] = sender
        else:
            self.senders[key_receiver] = {key_sender: sender}

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_event_received(self, **kwargs)


class RequestReceived(EventReceived):
    """The Request Received."""

    outputs: List[Parameter] = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        inputs: List[Parameter],
        outputs: List[Parameter],
        links: Dict[Link, List[Link]],
    ):
        super().__init__(component_impl_name, module_type_name, module_impl_name, language, name, inputs, links)
        self.outputs = outputs

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_request_received(self, **kwargs)


class VersionedData(Component):
    """The Versioned Data."""

    component_impl_name: str = None
    module_type_name: str = None
    module_impl_name: str = None
    language: str = None
    name: str = None
    type: str = None
    max_versions: int = None
    links: Dict[Link, List[Link]] = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        type: str,
        max_versions: int,
        links: Dict[Link, List[Link]],
    ):
        self.component_impl_name = component_impl_name
        self.module_type_name = module_type_name
        self.module_impl_name = module_impl_name
        self.language = language
        self.name = name
        self.type = type
        self.max_versions = max_versions
        self.links = links


class DataRead(VersionedData):
    """The Data Read."""

    notifying: bool = None
    writers: Dict = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        type: str,
        max_versions: int,
        notifying: bool,
        links: Dict[Link, List[Link]],
    ):
        super().__init__(
            component_impl_name, module_type_name, module_impl_name, language, name, type, max_versions, links
        )
        self.notifying = notifying
        self.writers = {}

    def add_writer(self, key_reader, key_writer, writer) -> None:
        if self.writers.get(key_reader):
            self.writers[key_reader][key_writer] = writer
        else:
            self.writers[key_reader] = {key_writer: writer}

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_data_read(self, **kwargs)


class DataWritten(VersionedData):
    """The Data Written."""

    write_only: bool = None
    readers: Dict = None
    links_written: Dict[Link, List[Link]] = None

    def __init__(
        self,
        component_impl_name: str,
        module_type_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        type: str,
        max_versions: int,
        write_only: bool,
        links: Dict[Link, List[Link]],
        links_written: Dict[Link, List[Link]],
    ):
        super().__init__(
            component_impl_name, module_type_name, module_impl_name, language, name, type, max_versions, links
        )
        self.write_only = write_only
        self.readers = {}
        self.links_written = links_written

    def add_reader(self, key_writer: str, key_reader: str, reader) -> None:
        if self.readers.get(key_writer):
            self.readers[key_writer][key_reader] = reader
        else:
            self.readers[key_writer] = {key_reader: reader}

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_data_written(self, **kwargs)


class Property(Variable):
    """The Property.

    Args:
        name: Property's name
        namespace: Property's namespace
        type: Property's type
        type_category: Property's type category
        component_impl_name: Property's component implementation name
        module_impl_name: Property's module implementation name
        language: Property's implementation language
        values: Property's values
    """

    component_impl_name: str = None
    module_impl_name: str = None
    language: str = None
    values: Dict = None

    def __init__(
        self,
        component_impl_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        namespace: str,
        type: str,
        type_category,
        values: Dict,
    ):
        super().__init__(name, namespace, type, type_category)
        self.component_impl_name = component_impl_name
        self.module_impl_name = module_impl_name
        self.language = language
        self.values = values

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_property(self, **kwargs)


class Pinfo(Component):
    """The Pinfo component."""

    component_impl_name: str = None
    module_impl_name: str = None
    language: str = None
    name: str = None
    is_private: bool = None
    values: Dict = None

    def __init__(
        self,
        component_impl_name: str,
        module_impl_name: str,
        language: str,
        name: str,
        is_private: bool,
        values: Dict,
    ):
        self.component_impl_name = component_impl_name
        self.module_impl_name = module_impl_name
        self.language = language
        self.name = name
        self.is_private = is_private
        self.values = values

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_pinfo(self, **kwargs)
