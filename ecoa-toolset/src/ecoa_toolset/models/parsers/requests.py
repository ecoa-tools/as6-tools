# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""RequestsParser class.
"""

from typing import Dict

# Internal library imports
from ecoa_toolset.models.components import Link, Parameter, RequestReceived, RequestSend
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class RequestsParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None
    _links: Dict[str, Dict] = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name
        self._links = {"clients": {}, "servers": {}}

    def _build_links(self, clients, server) -> None:
        client_links = [
            Link(
                client_type,
                client.instance_name,
                client.operation_name,
                getattr(client, "activating", True),
                None,
            )
            for client_type, clients_list in clients.items()
            for client in clients_list or []
        ]
        server_type, server_link = next(iter(server.items()))
        server_link = Link(
            server_type,
            server_link.instance_name,
            server_link.operation_name,
            getattr(server_link, "activating", True),
            None,
        )
        for client_link in client_links:
            self._links["clients"][client_link] = [server_link]
        self._links["servers"][server_link] = client_links

    def _build_all_links(self) -> None:
        for link in self._component_implementation.request_link:
            if getattr(link, "clients", "") and getattr(link, "server", ""):
                clients = {k: v for k, v in link.clients.__dict__.items() if v is not None}
                server = {k: v for k, v in link.server.__dict__.items() if v is not None}
                self._build_links(clients, server)

    def _build_request_sent(self, module_type, module_impl, module_inst_names, request_sent) -> None:
        request = RequestSend(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            request_sent.name,
            (
                getattr(request_sent, "is_synchronous")
                if "is_synchronous" in str(request_sent) and request_sent.is_synchronous
                else False
            ),
            self._ecoa_model.build_parameters(getattr(request_sent, "input", [])),
            self._ecoa_model.build_parameters(getattr(request_sent, "output", [])),
            {
                key: value
                for key, value in self._links["clients"].items()
                if key.type == "module_instance"
                and key.instance_name in module_inst_names
                and key.operation_name == request_sent.name
            },
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.requests_send:
            self._ecoa_model.requests_send[key].append(request)
        else:
            self._ecoa_model.requests_send[key] = [request]

    def _build_request_received(self, module_type, module_impl, module_inst_names, request_received) -> None:
        request = RequestReceived(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            request_received.name,
            (
                [Parameter("ID", "ECOA", "uint32", ecoa_types_2_0.Simple)]
                + self._ecoa_model.build_parameters(getattr(request_received, "input", []))
            ),
            self._ecoa_model.build_parameters(getattr(request_received, "output", [])),
            {
                key: value
                for key, value in self._links["servers"].items()
                if key.type == "module_instance"
                and key.instance_name in module_inst_names
                and key.operation_name == request_received.name
            },
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.requests_received:
            self._ecoa_model.requests_received[key].append(request)
        else:
            self._ecoa_model.requests_received[key] = [request]

    def _build_requests(self) -> None:
        for module_impl in self._component_implementation.module_implementation:
            module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
            module_inst_names = [
                module_inst.name
                for module_inst in self._component_implementation.module_instance
                if module_inst.implementation_name == module_impl.name
            ]
            for request_sent in module_type.operations.request_sent:
                self._build_request_sent(module_type, module_impl, module_inst_names, request_sent)
            for request_received in module_type.operations.request_received:
                self._build_request_received(module_type, module_impl, module_inst_names, request_received)

    def compute(self) -> None:
        if not (self._links.get("clients") and self._links.get("servers")):
            self._build_all_links()
        self._build_requests()
