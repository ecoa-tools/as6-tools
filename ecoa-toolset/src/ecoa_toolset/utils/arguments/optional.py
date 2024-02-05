# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The option argument implementation."""


class OptionalArgument:
    """The optional argument.

    Attributes:
        short_name (str): The short optional argument name.
        long_name (str): The long optional argument name.
        help (str): The optional argument help.
        action : The optional argument action.
        default (str): The optional argument default value.
        type : The optional argument type.
        choices : The optional argument choices.
        required (bool): The optional argument required.
    """

    short_name: str = None
    long_name: str = None
    help: str = None
    action = None
    default: str = None
    type = None
    choices = None
    required: bool = False

    def __init__(self, short_name: str, long_name: str, help_message: str, **kwargs):
        """The optional argument constructor.

        Args:
            short_name (str): The short optional argument name.
            long_name (str): The long optional argument name.
            help_message (str): The optional argument help.

        Kwargs:
            action (str): Argparse's action.
            default (str): The optional argument default value.
            type : The optional argument type.
            choices : The optional argument choices.
            required (bool): The optional argument required.
        """

        self.short_name = short_name
        self.long_name = long_name
        self.help = help_message
        self.action = kwargs.get("action")
        self.default = kwargs.get("default")
        self.type = kwargs.get("type")
        self.choices = kwargs.get("choices")
        self.required = kwargs.get("required")
