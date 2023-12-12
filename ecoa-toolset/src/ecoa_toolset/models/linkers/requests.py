# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""RequestsLinker class.
"""

# Standard library imports
from typing import List

# Internal library imports
from ecoa_toolset.models.components import Link, RequestReceived, RequestSend
from ecoa_toolset.models.linkers.common import CommonLinker


class RequestsLinker(CommonLinker):
    """"""

    def __init__(self, ecoa_model):
        super().__init__(ecoa_model)

    def _compare_links(
        self,
        send: RequestSend,
        send_sender_link: Link,
        send_receivers_links: List[Link],
        received: RequestReceived,
        received_receiver_link: Link,
        receiver_senders_links: List[Link],
    ) -> None:
        for send_receiver_link in send_receivers_links:
            for received_sender_link in receiver_senders_links:
                if send_receiver_link.type == "module_instance" and received_sender_link.type == "module_instance":
                    self._link_send_and_received_with_module_instances(
                        send,
                        send_sender_link,
                        send_receiver_link,
                        received,
                        received_receiver_link,
                        received_sender_link,
                    )
                elif send_receiver_link.type == "reference" and received_sender_link.type == "service":
                    self._link_send_and_received_with_services(
                        send,
                        send_sender_link,
                        send_receiver_link,
                        received,
                        received_receiver_link,
                        received_sender_link,
                    )

    def _compare_requests(self, send: RequestSend, received: RequestReceived) -> None:
        for send_sender_link, send_receivers_links in send.links.items():
            for received_receiver_link, received_senders_links in received.links.items():
                self._compare_links(
                    send,
                    send_sender_link,
                    send_receivers_links,
                    received,
                    received_receiver_link,
                    received_senders_links,
                )

    def compute(self) -> None:
        requests_send = [send for v in self._ecoa_model.requests_send.values() for send in v]
        requests_received = [received for v in self._ecoa_model.requests_received.values() for received in v]
        for send in requests_send:
            for received in requests_received:
                self._compare_requests(send, received)
