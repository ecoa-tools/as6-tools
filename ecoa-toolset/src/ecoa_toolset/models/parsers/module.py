# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""ModuleParser class.
"""

from typing import List

# Internal library imports
from ecoa_toolset.models.components import Log, Time


class ModuleParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name

    def _add_all_used_librairies(self, used_libraries: List) -> None:
        self._ecoa_model.use[self._component_impl_name] = [u.library for u in used_libraries]

    def _add_all_logs(self, module_type_name: str, module_impl_name: str, language: str) -> None:
        self._ecoa_model.logs[self._component_impl_name + ":" + module_impl_name] = Log(
            self._component_impl_name, module_type_name, module_impl_name, language.lower()
        )

    def _add_all_times(self, module_type_name: str, module_impl_name: str, language: str) -> None:
        self._ecoa_model.times[self._component_impl_name + ":" + module_impl_name] = Time(
            self._component_impl_name, module_type_name, module_impl_name, language.lower()
        )

    def compute(self) -> None:
        self._add_all_used_librairies(self._component_implementation.use)
        for module_impl in self._component_implementation.module_implementation:
            self._add_all_logs(module_impl.module_type, module_impl.name, module_impl.language)
            self._add_all_times(module_impl.module_type, module_impl.name, module_impl.language)
