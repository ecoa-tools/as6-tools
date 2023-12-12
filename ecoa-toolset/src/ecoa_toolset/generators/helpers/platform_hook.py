# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""PlatformHookHelper class.
"""

# Standard library imports
from typing import Any, Dict, List

# Internal library imports
from ecoa_toolset.models.components import Pinfo, Property


class PlatformHook:
    """The Platform Hook."""

    component_impl_name: str = None
    module_impl_name: str = None
    module_inst_name: str = None
    component_names: List[str] = None
    properties: List[Property] = []
    pinfos: List[Pinfo] = []
    language: str = None

    def __init__(
        self,
        component_impl_name,
        module_impl_name,
        module_inst_name,
        component_names,
        properties,
        pinfos,
        language,
        has_user_context,
        has_warm_start_context,
    ):
        self.component_impl_name = component_impl_name
        self.module_impl_name = module_impl_name
        self.module_inst_name = module_inst_name
        self.component_names = component_names
        self.properties = properties
        self.pinfos = pinfos
        self.language = language
        self.has_user_context = has_user_context
        self.has_warm_start_context = has_warm_start_context

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_hook(self, **kwargs)


class PlatformHookHelper:
    """Helper to manipulates platform hooks."""

    _ecoa_model = None
    _hooks: Dict[str, PlatformHook] = None

    def __init__(self, ecoa_model) -> None:
        self._ecoa_model = ecoa_model
        self._hooks = {}
        self._build_hooks()

    def _build_hooks(self):
        for key, module_inst in self._ecoa_model.module_insts.items():
            component_impl_name = ":".join(key.split(":")[:-1])
            module_impl = self._ecoa_model.module_impls.get(component_impl_name + ":" + module_inst.implementation_name)
            module_type = self._ecoa_model.module_types.get(component_impl_name + ":" + module_impl.module_type)
            self._hooks[key] = PlatformHook(
                component_impl_name,
                module_impl.name,
                module_inst.name,
                self._ecoa_model.component_names.get(key, []),
                self._ecoa_model.properties.get(component_impl_name + ":" + module_impl.name, []),
                self._ecoa_model.pinfos.get(component_impl_name + ":" + module_impl.name, []),
                module_impl.language.lower(),
                module_type.has_user_context,
                module_type.has_warm_start_context,
            )

    def find_all(
        self,
        component_impl_name: str = None,
        module_impl_name: str = None,
        module_inst_name: str = None,
        language: str = None,
    ):
        filtered = self._hooks
        if component_impl_name:
            filtered = {k: v for k, v in self._hooks.items() if v.component_impl_name == component_impl_name}
        if module_impl_name:
            filtered = {k: v for k, v in self._hooks.items() if v.module_impl_name == module_impl_name}
        if module_inst_name:
            filtered = {k: v for k, v in self._hooks.items() if v.module_inst_name == module_inst_name}
        if language is not None:
            filtered = {k: v for k, v in self._hooks.items() if v.language.lower() == language.lower()}
        return filtered
