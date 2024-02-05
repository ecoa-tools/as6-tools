# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The argument factory implementation."""

# Standard library imports
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import List

# Internal library imports
from ecoa_toolset.utils.arguments.optional import OptionalArgument
from ecoa_toolset.utils.arguments.positional import PositionalArgument

argparse_actions = [
    "store",
    "store_const",
    "store_true",
    "store_false",
    "append",
    "append_const",
    "count",
    "help",
    "version",
    "parsers",
    "extend",
]


class ArgumentParserError(Exception):
    """The ArgumentParserError Exception."""

    pass


class ThrowingArgumentParser(ArgumentParser):
    """The Throwing Argument Parser.

    This class is a subclass of ArgumentParser.
    """

    def error(self, message: str):
        """Override the error function of ArgumentParser to raise an exception instead of exiting.

        Args:
            message (str): The error message.

        Raise:
            ArgumentParserError
        """
        raise ArgumentParserError(message)


class ArgumentFactory:
    """The Argument Factory."""

    def create(
        description: str,
        positional_arguments: List[PositionalArgument],
        optional_arguments: List[OptionalArgument],
    ) -> ThrowingArgumentParser:
        """Creates an argument parser.

        Args:
            description: The argument parser description.
            positional_arguments: A list of PositionalArgument.
            optional_arguments: A list of OptionalArgument.

        Returns:
            ThrowingArgumentParser: The argument parser.
        """
        parser = ThrowingArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
        for option in positional_arguments:
            parser.add_argument(
                option.name,
                type=option.type,
                help=option.help,
            )
        for option in optional_arguments:
            if option.action in argparse_actions:
                parser.add_argument(
                    option.short_name,
                    option.long_name,
                    action=option.action,
                    help=option.help,
                )
            else:
                parser.add_argument(
                    option.short_name,
                    option.long_name,
                    nargs=None,
                    action=option.action,
                    default=option.default,
                    type=option.type,
                    choices=option.choices,
                    required=option.required,
                    help=option.help,
                )

        return parser
