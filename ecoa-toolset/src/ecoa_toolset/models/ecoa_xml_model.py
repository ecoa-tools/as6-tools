# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""ECOA XML Model.
"""

# Standard library imports
import logging
import os
import pathlib
from typing import Dict, List

# Internal library imports
from ecoa_toolset.models import ecoa_objects
from ecoa_toolset.models.ecoa_objects.ecoa_composite import ECOAComponentAssembly, ECOAServiceLink

# Third-Party library imports
from lxml import etree
from xsdata.formats.dataclass import parsers

logger = logging.getLogger(__name__)


class ECOAXMLModel:
    """Naive representation of ECOA XML.

    Attributes:
        _path (str): Path to the ECOA project file.
        _xml_parser (XmlParser): An XmlParser instance.
        _types (dict): The types dictionary (ecoa_types_2_0).
        _services (dict): The services dictionary (ecoa_interface_2_0.ServiceDefinition).
        _components (dict): The components dictionary (ecoa_implementation_2_0.ComponentImplementation).
        _assembly (dict): The assembly dictionary.
        _deployment (dict): The deployment dictionary.
        _components_assembly (list): The components assembly list.
        _wires (list): The wires list.
        _output (str): Path to the output directory.
    """

    _path: str = None
    _xml_parser: parsers.XmlParser = None
    _project = None
    _types: Dict = {}
    _services: Dict = {}
    _components: Dict = {}
    _assembly: Dict = {}
    _deployment: Dict = {}
    _components_assembly: Dict[str, ECOAComponentAssembly] = {}
    _wires: List[ECOAServiceLink] = []
    _output: str = None

    def __init__(self, path: str) -> None:
        """The ecoa xml model constructor.

        Args:
            path (str): Path to the ECOA project file.

        Returns:
            None.
        """

        self._path = path
        self._xml_parser = parsers.XmlParser(
            config=parsers.config.ParserConfig(
                fail_on_unknown_properties=True,
                fail_on_unknown_attributes=True,
                fail_on_converter_warnings=True,
            )
        )

    def _parse_types(self, project, directory) -> None:
        for type in project.types:
            for file in type.file:
                logger.info(f"\t{file}")
                self._types[file] = self._xml_parser.from_path(
                    pathlib.Path(os.path.join(directory, file)),
                    ecoa_objects.ecoa_types_2_0.Library,
                )

    def _parse_services(self, project, directory) -> None:
        for service in project.service_definitions:
            for file in service.file:
                logger.info(f"\t{file}")
                self._services[file] = self._xml_parser.from_path(
                    pathlib.Path(os.path.join(directory, file)),
                    ecoa_objects.ecoa_interface_2_0.ServiceDefinition,
                )

    def _parse_components(self, project, directory) -> None:
        for component in project.component_implementations:
            for file in component.file:
                logger.info(f"\t{file}")
                self._components[file] = self._xml_parser.from_path(
                    pathlib.Path(os.path.join(directory, file)),
                    ecoa_objects.ecoa_implementation_2_0.ComponentImplementation,
                )

    def _parse_assembly(self, project, directory) -> None:
        for file in project.implementation_assembly:
            logger.info(f"\t{file}")
            self._assembly[file] = etree.parse(os.path.join(directory, file))

    def _parse_deployement(self, project, directory) -> None:
        for file in project.deployment_schema:
            logger.info(f"\t{file}")
            self._deployment[file] = self._xml_parser.from_path(
                pathlib.Path(os.path.join(directory, file)),
                ecoa_objects.ecoa_deployment_2_0.Deployment,
            )

    def _set_component_instance_to_component_assembly(self, node, component_name: str) -> None:
        type_name = node.get("componentType")
        node_childs = node.getchildren()
        if node_childs:
            implementation_name = node_childs[0].get("name")
        else:
            implementation_name = None
        self._components_assembly[component_name].set_component_instance(type_name, implementation_name)

    def _get_property_value_from_assembly(self, name) -> str:
        for key, value in self._assembly.items():
            for child in self._assembly[key].getroot():
                if (
                    child.tag is not etree.Comment
                    and etree.QName(child).localname == "property"
                    and child.get("name") == name
                ):
                    return child.getchildren()[0].text
        return None

    def _add_property_to_component_assembly(self, node, component_name: str) -> None:
        property_name = node.get("name")
        property_source = node.get("source")
        property_value = (
            self._get_property_value_from_assembly(property_source[1:])
            if property_source
            else node.getchildren()[0].text
        )
        self._components_assembly[component_name].add_property(property_name, property_value)

    def _add_service_to_component_assembly(self, node, component_name: str) -> None:
        self._components_assembly[component_name].add_service(node.get("name"))

    def _build_component_assembly(self, node, component_name: str) -> None:
        if etree.QName(node).localname == "instance":
            self._set_component_instance_to_component_assembly(node, component_name)
        elif etree.QName(node).localname == "property":
            self._add_property_to_component_assembly(node, component_name)
        elif etree.QName(node).localname == "service" or etree.QName(node).localname == "reference":
            self._add_service_to_component_assembly(node, component_name)

    def _add_component_assembly(self, node) -> None:
        component_name = node.get("name")
        self._components_assembly[component_name] = ECOAComponentAssembly(component_name)
        for child in node.iter():
            if child.tag is not etree.Comment:
                self._build_component_assembly(child, component_name)

    def _parse_components_assembly(self) -> None:
        for key, value in self._assembly.items():
            for child in self._assembly[key].getroot():
                if child.tag is not etree.Comment and etree.QName(child).localname == "component":
                    self._add_component_assembly(child)

    def _get_component_service(self, service):
        for component_assembly in self._components_assembly.values():
            for component_service in component_assembly.services:
                if component_service.component_name + "/" + component_service.service_name == service:
                    return component_service
        return None

    def _parse_wires(self) -> None:
        for key, value in self._assembly.items():
            for child in self._assembly[key].getroot():
                if child.tag is not etree.Comment and etree.QName(child).localname == "wire":
                    source = self._get_component_service(child.get("source"))
                    target = self._get_component_service(child.get("target"))
                    self._wires.append(ECOAServiceLink(source, target))

    def read(self) -> None:
        """Reads an ECOA model and returns a MRT model.

        Args:
            None.

        Returns:
            None.
        """

        logger.info(f"Parsing {self._path}")
        directory = os.path.dirname(self._path)
        project = self._xml_parser.from_path(pathlib.Path(self._path), ecoa_objects.ecoa_project_2_0.Ecoaproject)
        self._project = project
        self._parse_types(project, directory)
        self._parse_services(project, directory)
        self._parse_components(project, directory)
        self._parse_assembly(project, directory)
        self._parse_deployement(project, directory)
        self._parse_components_assembly()
        self._parse_wires()
        self._output = project.output_directory

    def print_model(self):
        logger.debug("== PRINT TYPES ==")
        logger.debug(self._types)
        logger.debug("== PRINT SERVICES ==")
        logger.debug(self._services)
        logger.debug("== PRINT COMPONENTS ==")
        logger.debug(self._components)
        logger.debug("== PRINT DEPLOYMENT ==")
        logger.debug(self._deployment)
        logger.debug("== PRINT COMPONENTS ASSEMBLY ==")
        logger.debug(self._components_assembly)
        logger.debug("== PRINT WIRES ==")
        logger.debug(self._wires)
