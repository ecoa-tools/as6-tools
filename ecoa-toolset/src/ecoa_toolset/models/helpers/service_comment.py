# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Service Comment Helper class.
"""

# Standard library imports
from typing import List


class ServiceCommentHelper:
    """Helper to manipulates ECOA services comments."""

    _services = None

    def __init__(self, ecoa_model) -> None:
        self._services = ecoa_model.services

    def find_all(self, comment_category: str) -> List:
        """Search in ECOA model services comment.

        Args:
            - category (str)
                - Data
                - ResquestResponse
                - EventSent
                - EventReceived

        Returns:
            A list of comments

        Comments:
            cf. models/ecoa_objects/interface_2_0.py
        """
        filtered = None
        if comment_category == "Data":
            filtered = self.find_data_comment()
        elif comment_category == "ResquestResponse":
            filtered = self.find_request_response_comment()
        elif comment_category == "EventSent":
            filtered = self.find_event_comment(comment_category)
        elif comment_category == "EventReceived":
            filtered = self.find_event_comment(comment_category)

        return filtered

    def find_data_comment(self) -> List:
        """Search in ECOA Service data comments.

        Returns:
            data_comment: list of data comments


        Comments:
            cf. models/ecoa_objects/interface-2.0.py
        """

        data_comment = [
            data.comment
            for k, v in self._services.items()
            if v.operations.data
            for data in v.operations.data
            if data.comment
        ]

        return data_comment

    def find_request_response_comment(self) -> List:
        """Search in ECOA Service request-response comments.

        Returns:
            request_response_comment: list of request-response comments

        Comments:
            cf. models/ecoa_objects/interface-2.0.py
        """

        request_response_comment = [
            reqres.comment
            for k, v in self._services.items()
            if v.operations.requestresponse
            for reqres in v.operations.requestresponse
            if reqres.comment
        ]
        return request_response_comment

    def find_event_comment(self, comment_category: str) -> List:
        """Search in ECOA Service event received or sent comments.

        Returns:
            event_comment: list of event received or sent comments

        Comments:
            cf. models/ecoa_objects/interface-2.0.py
        """
        if comment_category == "EventReceived":
            comment_category = "RECEIVED_BY_PROVIDER"
        elif comment_category == "EventSent":
            comment_category = "SENT_BY_PROVIDER"

        event_comment = [
            event.comment
            for k, v in self._services.items()
            if v.operations.event
            for event in v.operations.event
            if event.comment and comment_category in str(event.direction)
        ]
        return event_comment
