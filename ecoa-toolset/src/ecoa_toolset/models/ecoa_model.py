# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""ECOA Model.
"""

# Standard library imports
import logging
import os
from typing import Dict, List

# Internal library imports
from ecoa_toolset.models.checkers.languages import LanguagesChecker
from ecoa_toolset.models.checkers.properties import PropertiesChecker
from ecoa_toolset.models.components import (
    DataRead,
    DataWritten,
    DynamicTriggerReceived,
    DynamicTriggerSend,
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
    Trigger,
)
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0
from ecoa_toolset.models.ecoa_xml_model import ECOAXMLModel
from ecoa_toolset.models.helpers.type import TypeHelper
from ecoa_toolset.models.linkers.data import DataLinker
from ecoa_toolset.models.linkers.events import EventsLinker
from ecoa_toolset.models.linkers.requests import RequestsLinker
from ecoa_toolset.models.parsers.data import DataParser
from ecoa_toolset.models.parsers.events import EventsParser
from ecoa_toolset.models.parsers.module import ModuleParser
from ecoa_toolset.models.parsers.pinfos import PinfosParser
from ecoa_toolset.models.parsers.properties import PropertiesParser
from ecoa_toolset.models.parsers.requests import RequestsParser

logger = logging.getLogger(__name__)


class ECOAModel:
    """The ECOA Model."""

    project_name: str = None
    project_path: str = None
    ecoa_xml_model: ECOAXMLModel = None
    types_helper: TypeHelper = None
    types: Dict = {}
    use: Dict = {}
    services: Dict = {}
    components: Dict = {}
    module_impls: Dict = {}
    module_types: Dict = {}
    module_insts: Dict = {}
    component_names: Dict[str, List[str]] = {}
    logs: Dict[str, Log] = {}
    times: Dict[str, Time] = {}
    events_received: Dict[str, List[EventReceived]] = {}
    events_send: Dict[str, List[EventSend]] = {}
    externals: Dict[str, List[External]] = {}
    triggers: Dict[str, List[Trigger]] = {}
    dynamic_triggers_received: Dict[str, List[DynamicTriggerReceived]] = {}
    dynamic_triggers_send: Dict[str, List[DynamicTriggerSend]] = {}
    requests_received: Dict[str, List[RequestReceived]] = {}
    requests_send: Dict[str, List[RequestSend]] = {}
    data_read: Dict[str, List[DataRead]] = {}
    data_written: Dict[str, List[DataWritten]] = {}
    properties: Dict[str, List[Property]] = {}
    pinfos: Dict[str, List[Pinfo]] = {}

    def __init__(self, project_name: str, path: str):
        self.project_name = project_name
        self.project_path = path
        self.ecoa_xml_model = ECOAXMLModel(path)
        self.ecoa_xml_model.read()
        if logger.root.level == logging.DEBUG:
            self.ecoa_xml_model.print_model()
        self.types_helper = TypeHelper(self)

    def get_component_count(self) -> int:
        return len(self.components)

    def get_module_count(self) -> int:
        return len(self.module_types)

    def _build_types(self, library_name: str, type_file: ecoa_types_2_0.Library) -> None:
        for type_category, types in type_file.types.__dict__.items():
            logger.debug(f"Parsing {type_category} types from {library_name}")
            for type in types:
                self.types[f"{library_name}:{type.name}"] = type

    def _parse_types(self) -> None:
        for type_file_path, type_file in self.ecoa_xml_model._types.items():
            library_name = os.path.basename(type_file_path).split(".")[0]
            self._build_types(library_name, type_file)

    def _parse_module_types(self) -> None:
        for path, component_implementation in self.components.items():
            component_impl_name = os.path.normpath(path).split(os.path.sep)[-2]
            for module_type in component_implementation.module_type:
                key = component_impl_name + ":" + module_type.name
                self.module_types[key] = module_type

    def _parse_module_implementations(self) -> None:
        for path, component_implementation in self.components.items():
            component_impl_name = os.path.normpath(path).split(os.path.sep)[-2]
            for module_impl in component_implementation.module_implementation:
                key = component_impl_name + ":" + module_impl.name
                self.module_impls[key] = module_impl

    def _parse_module_instances(self) -> None:
        for path, component_implementation in self.components.items():
            component_impl_name = os.path.normpath(path).split(os.path.sep)[-2]
            for module_inst in component_implementation.module_instance:
                key = component_impl_name + ":" + module_inst.name
                self.module_insts[key] = module_inst

    def _add_component_name(self, deployed_module_instance):
        component_name = deployed_module_instance.component_name
        module_inst_name = deployed_module_instance.module_instance_name
        component_impl_name = self.ecoa_xml_model._components_assembly.get(
            component_name
        ).component_instance.implementation_name
        key = component_impl_name + ":" + module_inst_name
        if key in self.component_names:
            self.component_names[key].append(component_name)
        else:
            self.component_names[key] = [component_name]

    def _parse_component_names(self):
        for v in self.ecoa_xml_model._deployment.values():
            for pd in v.protection_domain:
                for dmi in pd.deployed_module_instance:
                    self._add_component_name(dmi)

    def parse(self) -> None:
        """Parses types and component implementations.

        Args:
            None.

        Returns:
            None.

        Comments:
            cf. models/ecoa_objects/ecoa_types_2_0.py
            cf. models/ecoa_objects/ecoa_implementation_2_0.py
        """
        self.components = self.ecoa_xml_model._components
        self._parse_types()
        self._parse_module_types()
        self._parse_module_implementations()
        self._parse_module_instances()
        self._parse_component_names()
        LanguagesChecker(self).compute()
        for path, component_implementation in self.components.items():
            component_impl_name = os.path.normpath(path).split(os.path.sep)[-2]
            logger.debug(f"Parsing component implementation: {component_impl_name}")
            ModuleParser(self, component_implementation, component_impl_name).compute()
            EventsParser(self, component_implementation, component_impl_name).compute()
            RequestsParser(self, component_implementation, component_impl_name).compute()
            DataParser(self, component_implementation, component_impl_name).compute()
            PropertiesParser(self, component_implementation, component_impl_name).compute()
            PinfosParser(self, component_implementation, component_impl_name, path).compute()
        PropertiesChecker(self).compute()
        EventsLinker(self).compute()
        RequestsLinker(self).compute()
        DataLinker(self).compute()
        self._redirect_dynamic_triggers()
        logger.debug(f"Total number of event received: {len(self.events_received)}")
        logger.debug(f"Total number of event send: {len(self.events_send)}")
        logger.debug(f"Total number of request received: {len(self.requests_received)}")
        logger.debug(f"Total number of request send: {len(self.requests_send)}")

    def build_parameters(self, parameters: List) -> None:
        """Build the list of parameters.

        Args:
            parameters (inputs or outputs from an operation of module_type.operations) : The parameters.

        Returns:
            parameters (List[Parameter]) : The parameters.
        """
        liste = []
        for param in parameters:
            parameter_type = self.types_helper.add_namespace(param.type)
            parameter = Parameter(
                param.name,
                self.types_helper.get_namespace(parameter_type),
                self.types_helper.get_name(parameter_type),
                self.types_helper.get_type_category(parameter_type),
            )
            liste.append(parameter)
        return liste

    def _find_final_receivers(self, component_impl_name: str, name: str) -> Dict:
        for dynamic_trigger in self.dynamic_triggers_send.get(component_impl_name):
            if dynamic_trigger.name == name:
                for key_sender, receivers in dynamic_trigger.receivers.items():
                    if key_sender.split(":")[1] == "out":
                        return receivers
        return {}

    def _redirect_dynamic_triggers(self) -> None:
        events_send = [send for v in self.events_send.values() for send in v]
        for send in events_send:
            for key_sender, receivers in send.receivers.copy().items():
                for key_receiver, receiver in receivers.copy().items():
                    if isinstance(receiver, DynamicTriggerReceived):
                        if key_receiver.split(":")[1] == "in":
                            final_receivers = self._find_final_receivers(receiver.component_impl_name, receiver.name)
                            for key_final_receiver, final_receiver in final_receivers.items():
                                send.add_receiver(key_sender, key_final_receiver, final_receiver)
                        del send.receivers[key_sender][key_receiver]
                if not send.receivers[key_sender]:
                    del send.receivers[key_sender]
        externals = [external for v in self.externals.values() for external in v]
        for external in externals:
            for key_receiver, receiver in external.receivers.copy().items():
                if isinstance(receiver, DynamicTriggerReceived):
                    if key_receiver.split(":")[1] == "in":
                        final_receivers = self._find_final_receivers(receiver.component_impl_name, receiver.name)
                        for key_final_receiver, final_receiver in final_receivers.items():
                            external.add_receiver(key_final_receiver, final_receiver)
                    del external.receivers[key_receiver]
