# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The positional argument implementation."""

from typing import Type


class PositionalArgument:
    """The positional argument.

    Attributes:
        name (str): The argument name.
        type (Type): The argument type.
        help (str): The argument help.
    """

    name: str = None
    type: Type = None
    help: str = None

    def __init__(self, name: str, type: Type, help: str):
        """The argument constructor.

        Args:
            name (str): The argument name.
            type (Type): The argument type.
            help (str): The argument help.
        """

        self.name = name
        self.type = type
        self.help = help
