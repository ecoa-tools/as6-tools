# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The custom action implementations."""

# Standard library imports
import argparse


class Once(argparse.Action):
    """The Once action."""

    def __init__(self, option_strings, dest, **kwargs):
        """The Once action constructor."""

        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """The Once action call function.

        Args:
            parser : The parser.
            namespace : The namespace.
            values : The values.
            option_string (optional): The option strings.

        Raise:
            argparse.ArgumentError
        """
        if hasattr(self, "seen"):
            raise argparse.ArgumentError(self, "argument duplicated")
        setattr(self, "seen", True)
        setattr(namespace, self.dest, values)


class OnceAndStoreTrue(argparse.Action):
    """The Once and StoreTrue action."""

    def __init__(self, option_strings, dest, **kwargs):
        """The Once and StoreTrue action constructor."""

        if "nargs" in kwargs:
            del kwargs["nargs"]
        if "const" in kwargs:
            del kwargs["const"]
        if "default" in kwargs:
            del kwargs["default"]
        if "type" in kwargs:
            del kwargs["type"]
        if "choices" in kwargs:
            del kwargs["choices"]
        if "required" in kwargs:
            del kwargs["required"]
        super().__init__(option_strings, dest, nargs=0, const=True, default=False, type=bool, choices=None, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """The Once and StoreTrue action call function.

        Args:
            parser : The parser.
            namespace : The namespace.
            values : The values.
            option_string (optional): The option strings.

        Raise:
            argparse.ArgumentError
        """
        if hasattr(self, "seen"):
            raise argparse.ArgumentError(self, "argument duplicated")
        setattr(self, "seen", True)
        setattr(namespace, self.dest, True)
