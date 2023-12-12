# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""CommonLinker class.
"""

from typing import Any

# Internal library imports
from ecoa_toolset.models.components import Link


class CommonLinker:
    """"""

    _ecoa_model = None

    def __init__(self, ecoa_model):
        self._ecoa_model = ecoa_model

    def _link_send_and_received_with_module_instances(
        self,
        send: Any,
        send_sender_link: Link,
        send_receiver_link: Link,
        received: Any,
        received_receiver_link: Link,
        received_sender_link: Link,
    ) -> None:
        if send.component_impl_name == received.component_impl_name:
            if send_sender_link == received_sender_link and received_receiver_link == send_receiver_link:
                sender_component_names = self._ecoa_model.component_names.get(
                    send.component_impl_name + ":" + send_sender_link.instance_name, []
                )
                received_component_names = self._ecoa_model.component_names.get(
                    received.component_impl_name + ":" + received_receiver_link.instance_name, []
                )
                for sender_component_name in sender_component_names:
                    for received_component_name in received_component_names:
                        key_sender = send_sender_link.instance_name + ":" + sender_component_name
                        key_receiver = received_receiver_link.instance_name + ":" + received_component_name
                        send.add_receiver(key_sender, key_receiver, received)
                        received.add_sender(key_receiver, key_sender, send)

    def _link_send_and_received_with_services(
        self,
        send: Any,
        send_sender_link: Link,
        send_receiver_link: Link,
        received: Any,
        received_receiver_link: Link,
        received_sender_link: Link,
    ) -> None:
        sender_component_names = self._ecoa_model.component_names.get(
            send.component_impl_name + ":" + send_sender_link.instance_name
        )
        received_component_names = self._ecoa_model.component_names.get(
            received.component_impl_name + ":" + received_receiver_link.instance_name
        )
        if not sender_component_names or not received_component_names:
            return
        if send_receiver_link.operation_name == received_sender_link.operation_name:
            for wire in self._ecoa_model.ecoa_xml_model._wires:
                key = None
                if (
                    wire.source.component_name in sender_component_names
                    and wire.source.service_name == send_receiver_link.instance_name
                    and wire.target.component_name in received_component_names
                    and wire.target.service_name == received_sender_link.instance_name
                ):
                    key = (
                        send_sender_link.instance_name
                        + ":"
                        + wire.source.component_name
                        + "::"
                        + received_receiver_link.instance_name
                        + ":"
                        + wire.target.component_name
                    )
                elif (
                    wire.source.component_name in received_component_names
                    and wire.source.service_name == received_sender_link.instance_name
                    and wire.target.component_name in sender_component_names
                    and wire.target.service_name == send_receiver_link.instance_name
                ):
                    key = (
                        send_sender_link.instance_name
                        + ":"
                        + wire.target.component_name
                        + "::"
                        + received_receiver_link.instance_name
                        + ":"
                        + wire.source.component_name
                    )
                if key:
                    key_sender, key_receiver = tuple(key.split("::"))
                    send.add_receiver(key_sender, key_receiver, received)
                    received.add_sender(key_receiver, key_sender, send)
