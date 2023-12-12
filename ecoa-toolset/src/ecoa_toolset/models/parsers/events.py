# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""EventsParser class.
"""

from typing import Dict

# Internal library imports
from ecoa_toolset.models.components import (
    DynamicTriggerReceived,
    DynamicTriggerSend,
    EventReceived,
    EventSend,
    External,
    Link,
    Parameter,
    Trigger,
)
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class EventsParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None
    _links: Dict[str, Dict] = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name
        self._links = {"senders": {}, "receivers": {}}

    def _build_links(self, senders, receivers) -> None:
        sender_links = [
            Link(
                sender_type,
                getattr(sender, "instance_name", ""),
                getattr(sender, "operation_name", ""),
                getattr(sender, "activating", True),
                getattr(sender, "language", "").lower(),
            )
            for sender_type, senders_list in senders.items()
            for sender in senders_list or []
        ]
        receiver_links = [
            Link(
                receiver_type,
                receiver.instance_name,
                receiver.operation_name,
                getattr(receiver, "activating", True),
                None,
            )
            for receiver_type, receivers_list in receivers.items()
            for receiver in receivers_list or []
        ]
        for sender_link in sender_links:
            self._links["senders"][sender_link] = receiver_links
        for receiver_link in receiver_links:
            self._links["receivers"][receiver_link] = sender_links

    def _build_all_links(self) -> None:
        for link in self._component_implementation.event_link:
            if getattr(link, "senders", "") and getattr(link, "receivers", ""):
                senders = {k: v for k, v in link.senders.__dict__.items() if v is not None}
                receivers = {k: v for k, v in link.receivers.__dict__.items() if v is not None}
                self._build_links(senders, receivers)

    def _build_event_sent(self, module_type, module_impl, module_inst_names, event_sent) -> None:
        event = EventSend(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            event_sent.name,
            self._ecoa_model.build_parameters(getattr(event_sent, "input", [])),
            {
                key: value
                for key, value in self._links["senders"].items()
                if key.type == "module_instance"
                and key.instance_name in module_inst_names
                and key.operation_name == event_sent.name
            },
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.events_send:
            self._ecoa_model.events_send[key].append(event)
        else:
            self._ecoa_model.events_send[key] = [event]

    def _build_event_received(self, module_type, module_impl, module_inst_names, event_received) -> None:
        event = EventReceived(
            self._component_impl_name,
            module_type.name,
            module_impl.name,
            module_impl.language.lower(),
            event_received.name,
            self._ecoa_model.build_parameters(getattr(event_received, "input", [])),
            {
                key: value
                for key, value in self._links["receivers"].items()
                if key.type == "module_instance"
                and key.instance_name in module_inst_names
                and key.operation_name == event_received.name
            },
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.events_received:
            self._ecoa_model.events_received[key].append(event)
        else:
            self._ecoa_model.events_received[key] = [event]

    def _build_events(self) -> None:
        for module_impl in self._component_implementation.module_implementation:
            module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
            module_inst_names = [
                module_inst.name
                for module_inst in self._component_implementation.module_instance
                if module_inst.implementation_name == module_impl.name
            ]
            for event_sent in module_type.operations.event_sent:
                self._build_event_sent(module_type, module_impl, module_inst_names, event_sent)
            for event_received in module_type.operations.event_received:
                self._build_event_received(module_type, module_impl, module_inst_names, event_received)

    def _build_externals(self) -> None:
        externals = {}
        for sender_link in self._links["senders"].keys():
            if sender_link.type == "external":
                key_external = self._component_impl_name + ":" + sender_link.operation_name + ":" + sender_link.language
                externals[key_external] = External(
                    self._component_impl_name,
                    sender_link.operation_name,
                    sender_link.language,
                    {
                        key: value
                        for key, value in self._links["senders"].items()
                        if key.type == "external"
                        and key.operation_name == sender_link.operation_name
                        and key.language == sender_link.language
                    },
                )
        for key_external, external in externals.items():
            key = key_external.split(":")[0]
            if key in self._ecoa_model.externals:
                self._ecoa_model.externals[key].append(external)
            else:
                self._ecoa_model.externals[key] = [external]

    def _build_triggers(self) -> None:
        key = self._component_impl_name
        for trigger_instance in self._component_implementation.trigger_instance:
            trigger = Trigger(
                self._component_impl_name,
                trigger_instance.name,
                {
                    key: value
                    for key, value in self._links["senders"].items()
                    if key.type == "trigger" and key.instance_name == trigger_instance.name
                },
            )
            if key in self._ecoa_model.triggers:
                self._ecoa_model.triggers[key].append(trigger)
            else:
                self._ecoa_model.triggers[key] = [trigger]

    def _build_dynamic_triggers(self) -> None:
        key = self._component_impl_name
        for dynamic_trigger_instance in self._component_implementation.dynamic_trigger_instance:
            name = dynamic_trigger_instance.name
            parameters = [
                Parameter("delayDuration", "ECOA", "duration", ecoa_types_2_0.Record)
            ] + self._ecoa_model.build_parameters(getattr(dynamic_trigger_instance, "parameter", []))
            dynamic_trigger_send = DynamicTriggerSend(
                key,
                name,
                parameters,
                {
                    key: value
                    for key, value in self._links["senders"].items()
                    if key.type == "dynamic_trigger" and key.instance_name == dynamic_trigger_instance.name
                },
            )
            dynamic_trigger_received = DynamicTriggerReceived(
                key,
                name,
                parameters,
                {
                    key: value
                    for key, value in self._links["receivers"].items()
                    if key.type == "dynamic_trigger" and key.instance_name == dynamic_trigger_instance.name
                },
            )
            if key in self._ecoa_model.dynamic_triggers_send:
                self._ecoa_model.dynamic_triggers_send[key].append(dynamic_trigger_send)
            else:
                self._ecoa_model.dynamic_triggers_send[key] = [dynamic_trigger_send]
            if key in self._ecoa_model.dynamic_triggers_received:
                self._ecoa_model.dynamic_triggers_received[key].append(dynamic_trigger_received)
            else:
                self._ecoa_model.dynamic_triggers_received[key] = [dynamic_trigger_received]

    def compute(self) -> None:
        if not (self._links.get("senders") and self._links.get("receivers")):
            self._build_all_links()
        self._build_events()
        self._build_externals()
        self._build_triggers()
        self._build_dynamic_triggers()
