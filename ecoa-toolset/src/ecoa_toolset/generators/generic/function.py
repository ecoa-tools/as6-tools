# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Function Generator base class.
"""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Any

# Internal library imports
from ecoa_toolset.generators.common import Common


class FunctionGenerator(ABC):
    """Base class for all function's generators."""

    indent_level: int = None
    indent_step: int = None
    body: bool = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__()
        self.indent_level = indent_level
        self.indent_step = indent_step
        self.body = body

    @abstractmethod
    def _generate_prototype(self, element: Any) -> str:
        pass

    @abstractmethod
    def _generate_body(self, element: Any) -> str:
        pass

    def generate(self, element: Any) -> str:
        """"""
        generation = self._generate_prototype(element)
        if self.body:
            generation += (
                Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[: self.indent_level] + "{" + Common.LINE_BREAK[:1]
            )
            self.indent_level += self.indent_step
            generation += self._generate_body(element) + Common.LINE_BREAK[:1]
            self.indent_level -= self.indent_step
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "}"
        else:
            generation += ";"
        generation += Common.LINE_BREAK[:2]
        return generation
