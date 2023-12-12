# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""EventsLinker class.
"""

from typing import Any, List

# Internal library imports
from ecoa_toolset.models.components import (
    DynamicTriggerReceived,
    DynamicTriggerSend,
    EventReceived,
    EventSend,
    External,
    Link,
    Trigger,
)
from ecoa_toolset.models.linkers.common import CommonLinker


class EventsLinker(CommonLinker):
    """"""

    def __init__(self, ecoa_model):
        super().__init__(ecoa_model)

    def _link_external_and_event_received(
        self,
        external: External,
        external_sender_link: Link,
        external_receiver_link: Link,
        received: EventReceived,
        received_receiver_link: Link,
        received_sender_link: Link,
    ) -> None:
        if external_sender_link == received_sender_link and received_receiver_link == external_receiver_link:
            received_component_names = self._ecoa_model.component_names.get(
                received.component_impl_name + ":" + received_receiver_link.instance_name, []
            )
            key_sender = external_sender_link.operation_name + ":" + external_sender_link.language
            for received_component_name in received_component_names:
                key_receiver = received_receiver_link.instance_name + ":" + received_component_name
                external.add_receiver(key_receiver, received)
                received.add_sender(key_receiver, key_sender, external)
                if not external.inputs:
                    external.inputs = received.inputs

    def _link_external_and_dynamic_trigger(
        self,
        external: External,
        external_sender_link: Link,
        external_receiver_link: Link,
        dynamic_trigger: DynamicTriggerReceived,
        dynamic_trigger_receiver_link: Link,
        dynamic_trigger_sender_link: Link,
    ) -> None:
        if (
            external_sender_link == dynamic_trigger_sender_link
            and dynamic_trigger_receiver_link == external_receiver_link
        ):
            key_sender = external_sender_link.operation_name + ":" + external_sender_link.language
            key_receiver = (
                dynamic_trigger_receiver_link.instance_name + ":" + dynamic_trigger_receiver_link.operation_name
            )
            external.add_receiver(key_receiver, dynamic_trigger)
            dynamic_trigger.add_sender(key_receiver, key_sender, external)
            if not external.inputs:
                external.inputs = dynamic_trigger.parameters

    def _link_trigger_and_event_received(
        self,
        trigger: Trigger,
        trigger_sender_link: Link,
        trigger_receiver_link: Link,
        received: EventReceived,
        received_receiver_link: Link,
        received_sender_link: Link,
    ) -> None:
        if trigger_sender_link == received_sender_link and received_receiver_link == trigger_receiver_link:
            received_component_names = self._ecoa_model.component_names.get(
                received.component_impl_name + ":" + received_receiver_link.instance_name, []
            )
            key_sender = trigger_sender_link.instance_name
            for received_component_name in received_component_names:
                key_receiver = received_receiver_link.instance_name + ":" + received_component_name
                trigger.add_receiver(key_receiver, received)
                received.add_sender(key_receiver, key_sender, trigger)

    def _link_dynamic_trigger_and_event_received(
        self,
        dynamic_trigger: DynamicTriggerSend,
        dynamic_trigger_sender_link: Link,
        dynamic_trigger_receiver_link: Link,
        received: EventReceived,
        received_receiver_link: Link,
        received_sender_link: Link,
    ) -> None:
        if (
            dynamic_trigger_sender_link == received_sender_link
            and received_receiver_link == dynamic_trigger_receiver_link
        ):
            received_component_names = self._ecoa_model.component_names.get(
                received.component_impl_name + ":" + received_receiver_link.instance_name, []
            )
            key_sender = dynamic_trigger_sender_link.instance_name + ":" + dynamic_trigger_sender_link.operation_name
            for received_component_name in received_component_names:
                key_receiver = received_receiver_link.instance_name + ":" + received_component_name
                dynamic_trigger.add_receiver(key_sender, key_receiver, received)
                received.add_sender(key_receiver, key_sender, dynamic_trigger)

    def _link_event_send_and_dynamic_trigger(
        self,
        send: EventSend,
        send_sender_link: Link,
        send_receiver_link: Link,
        dynamic_trigger: DynamicTriggerReceived,
        dynamic_trigger_receiver_link: Link,
        dynamic_trigger_sender_link: Link,
    ) -> None:
        if send_sender_link == dynamic_trigger_sender_link and dynamic_trigger_receiver_link == send_receiver_link:
            send_component_names = self._ecoa_model.component_names.get(
                send.component_impl_name + ":" + send_sender_link.instance_name, []
            )
            key_receiver = (
                dynamic_trigger_receiver_link.instance_name + ":" + dynamic_trigger_receiver_link.operation_name
            )
            for send_component_name in send_component_names:
                key_sender = send_sender_link.instance_name + ":" + send_component_name
                send.add_receiver(key_sender, key_receiver, dynamic_trigger)
                dynamic_trigger.add_sender(key_receiver, key_sender, send)

    def _compare_events_links(
        self,
        send: Any,
        send_sender_link: Link,
        send_receivers_links: List[Link],
        received: Any,
        received_receiver_link: Link,
        receiver_senders_links: List[Link],
    ) -> None:
        for send_receiver_link in send_receivers_links:
            for received_sender_link in receiver_senders_links:
                if isinstance(send, EventSend) and isinstance(received, EventReceived):
                    if send_receiver_link.type == "module_instance" and received_sender_link.type == "module_instance":
                        self._link_send_and_received_with_module_instances(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                    elif (send_receiver_link.type == "reference" or send_receiver_link.type == "service") and (
                        received_sender_link.type == "reference" or received_sender_link.type == "service"
                    ):
                        self._link_send_and_received_with_services(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                elif isinstance(send, External) and isinstance(received, EventReceived):
                    if send_receiver_link.type == "module_instance" and received_sender_link.type == "external":
                        self._link_external_and_event_received(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                elif isinstance(send, External) and isinstance(received, DynamicTriggerReceived):
                    if send_receiver_link.type == "dynamic_trigger" and received_sender_link.type == "external":
                        self._link_external_and_dynamic_trigger(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                elif isinstance(send, Trigger) and isinstance(received, EventReceived):
                    if send_receiver_link.type == "module_instance" and received_sender_link.type == "trigger":
                        self._link_trigger_and_event_received(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                elif isinstance(send, DynamicTriggerSend) and isinstance(received, EventReceived):
                    if send_receiver_link.type == "module_instance" and received_sender_link.type == "dynamic_trigger":
                        self._link_dynamic_trigger_and_event_received(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )
                elif isinstance(send, EventSend) and isinstance(received, DynamicTriggerReceived):
                    if send_receiver_link.type == "dynamic_trigger" and received_sender_link.type == "module_instance":
                        self._link_event_send_and_dynamic_trigger(
                            send,
                            send_sender_link,
                            send_receiver_link,
                            received,
                            received_receiver_link,
                            received_sender_link,
                        )

    def _compare_events(self, send: Any, received: Any) -> None:
        for send_sender_link, send_receivers_links in send.links.items():
            for received_receiver_link, received_senders_links in received.links.items():
                self._compare_events_links(
                    send,
                    send_sender_link,
                    send_receivers_links,
                    received,
                    received_receiver_link,
                    received_senders_links,
                )

    def _link_events(self) -> None:
        events_send = [send for v in self._ecoa_model.events_send.values() for send in v]
        events_received = [received for v in self._ecoa_model.events_received.values() for received in v]
        for send in events_send:
            for received in events_received:
                self._compare_events(send, received)

    def _link_externals_and_events_received(self) -> None:
        for key, externals in self._ecoa_model.externals.items():
            events_received = [
                received
                for k, v in self._ecoa_model.events_received.items()
                for received in v
                if k.split(":")[0] == key
            ]
            for external in externals:
                for received in events_received:
                    self._compare_events(external, received)

    def _link_externals_and_dynamic_triggers(self) -> None:
        for key, externals in self._ecoa_model.externals.items():
            dynamic_triggers_received = [
                dynamic_trigger
                for k, v in self._ecoa_model.dynamic_triggers_received.items()
                for dynamic_trigger in v
                if k == key
            ]
            for external in externals:
                for dynamic_trigger_received in dynamic_triggers_received:
                    self._compare_events(external, dynamic_trigger_received)

    def _link_triggers_and_events_received(self) -> None:
        for key, triggers in self._ecoa_model.triggers.items():
            events_received = [
                received
                for k, v in self._ecoa_model.events_received.items()
                for received in v
                if k.split(":")[0] == key
            ]
            for trigger in triggers:
                for received in events_received:
                    self._compare_events(trigger, received)

    def _link_dynamic_triggers_and_events_received(self) -> None:
        for key, dynamic_triggers_send in self._ecoa_model.dynamic_triggers_send.items():
            events_received = [
                received
                for k, v in self._ecoa_model.events_received.items()
                for received in v
                if k.split(":")[0] == key
            ]
            for dynamic_trigger_send in dynamic_triggers_send:
                for received in events_received:
                    self._compare_events(dynamic_trigger_send, received)

    def _link_events_send_and_dynamic_triggers(self) -> None:
        for key, dynamic_triggers_received in self._ecoa_model.dynamic_triggers_received.items():
            events_send = [
                send for k, v in self._ecoa_model.events_send.items() for send in v if k.split(":")[0] == key
            ]
            for send in events_send:
                for dynamic_trigger_received in dynamic_triggers_received:
                    self._compare_events(send, dynamic_trigger_received)

    def compute(self) -> None:
        self._link_events()
        self._link_externals_and_events_received()
        self._link_externals_and_dynamic_triggers()
        self._link_triggers_and_events_received()
        self._link_dynamic_triggers_and_events_received()
        self._link_events_send_and_dynamic_triggers()
