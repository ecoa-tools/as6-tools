# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""PinfosParser class.
"""

import os
from typing import Dict

# Internal library imports
from ecoa_toolset.models.components import Pinfo


class PinfosParser:
    """"""

    _ecoa_model = None
    _component_implementation = None
    _component_impl_name: str = None
    _path: str = None

    def __init__(self, ecoa_model, component_implementation, component_impl_name: str, path: str):
        self._ecoa_model = ecoa_model
        self._component_implementation = component_implementation
        self._component_impl_name = component_impl_name
        self._path = path

    def _build_path(self, pinfo_value: str, is_private: bool) -> str:
        if is_private:
            return os.path.join(
                os.path.dirname(self._ecoa_model.project_path),
                os.path.dirname(self._path),
                "Pinfo",
                pinfo_value.replace('"', ""),
            )
        return os.path.join(
            os.path.dirname(self._ecoa_model.project_path), "5-Integration", "Pinfo", pinfo_value.replace('"', "")
        )

    def _build_values(self, module_impl, pinfo, is_private: bool) -> Dict:
        pinfo_values = {}
        for key, module_inst in self._ecoa_model.module_insts.items():
            if (
                self._component_impl_name == ":".join(key.split(":")[:-1])
                and module_inst.implementation_name == module_impl.name
            ):
                for pi in module_inst.pinfo.public_pinfo + module_inst.pinfo.private_pinfo:
                    if pi.name == pinfo.name:
                        pinfo_values[key] = pi.value.strip()
                        break
        tmp = {}
        for key, pinfo_value in pinfo_values.items():
            for component_name in self._ecoa_model.component_names.get(key, []):
                k = key + ":" + component_name
                if pinfo_value[0] == "$":
                    for ci in self._ecoa_model.ecoa_xml_model._components_assembly.values():
                        if ci.name == component_name:
                            tmp[k] = self._build_path(ci.properties[pinfo_value[1:]], is_private)
                else:
                    tmp[k] = self._build_path(pinfo_value, is_private)
            else:
                tmp[key] = self._build_path(pinfo_value, is_private)
        pinfo_values = tmp
        return pinfo_values

    def _build(self, module_impl, pinfo, is_private: bool) -> None:
        pinfo_values = self._build_values(module_impl, pinfo, is_private)
        pinfo = Pinfo(
            self._component_impl_name,
            module_impl.name,
            module_impl.language.lower(),
            pinfo.name,
            is_private,
            pinfo_values,
        )
        key = self._component_impl_name + ":" + module_impl.name
        if key in self._ecoa_model.pinfos:
            self._ecoa_model.pinfos[key].append(pinfo)
        else:
            self._ecoa_model.pinfos[key] = [pinfo]

    def _add_all(self, module_impl, pinfos, is_private: bool = False) -> None:
        for pinfo in pinfos:
            self._build(module_impl, pinfo, is_private)

    def compute(self) -> None:
        for module_impl in self._component_implementation.module_implementation:
            module_type = self._ecoa_model.module_types.get(self._component_impl_name + ":" + module_impl.module_type)
            if module_type.pinfo and module_type.pinfo.public_pinfo:
                self._add_all(module_impl, module_type.pinfo.public_pinfo)
            if module_type.pinfo and module_type.pinfo.private_pinfo:
                self._add_all(module_impl, module_type.pinfo.private_pinfo, is_private=True)
