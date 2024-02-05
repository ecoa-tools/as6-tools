# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

""" Strategy design pattern classes.
"""

# Standard library imports
from abc import ABC, abstractmethod


class Strategy(ABC):
    """Base class for all strategies."""

    @abstractmethod
    def execute(self):
        pass


class Context:
    """Context that hold a specific strategy."""

    _strategy: Strategy = None

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute(self) -> None:
        self._strategy.execute()
