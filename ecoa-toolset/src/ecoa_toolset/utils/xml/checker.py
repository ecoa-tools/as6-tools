# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The XML checker implementation."""

from lxml.etree import DocumentInvalid, XMLSchema, _ElementTree


class Checker:
    """The XML Checker."""

    @staticmethod
    def is_valid(xml_file: _ElementTree, xml_schema: XMLSchema) -> bool:
        """Check if an xml file fits its schema.

        Args:
            xml_file (_ElementTree): The xml file.
            xml_schema (XMLSchema): The xml schema.

        Returns:
            bool: The validity of the xml file.
        """

        try:
            xml_schema.assertValid(xml_file)
        except DocumentInvalid:
            return False
        return True
