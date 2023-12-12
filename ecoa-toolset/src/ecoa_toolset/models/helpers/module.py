# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""ModuleHelper class.
"""

# Standard library imports
from typing import List


class ModuleHelper:
    """Helper to manipulates ECOA modules."""

    _ecoa_model = None

    def __init__(self, ecoa_model) -> None:
        self._ecoa_model = ecoa_model

    def find_all(self, language=None, fault_handler=False, warm_start_context=False) -> List:
        """Search in ECOA model modules.

        Returns:
            A list of modules

        Comments:
            cf. models/ecoa_objects/implementation-2.0.py
        """
        modules = self._ecoa_model.module_impls
        if language:
            modules = {k: v for k, v in modules.items() if v.language.lower() == language.lower()}
        if fault_handler:
            modules = {
                k: v
                for k, v in modules.items()
                if self._ecoa_model.module_types.get(":".join(k.split(":")[:-1]) + ":" + v.module_type).is_fault_handler
            }
        if warm_start_context:
            modules = {
                k: v
                for k, v in modules.items()
                if self._ecoa_model.module_types.get(
                    ":".join(k.split(":")[:-1]) + ":" + v.module_type
                ).has_warm_start_context
            }
        return modules
