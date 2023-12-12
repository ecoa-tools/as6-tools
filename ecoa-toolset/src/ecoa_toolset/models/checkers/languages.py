# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""LanguagesChecker class.
"""


class LanguagesChecker:
    """Checker of module implementation languages.

    Args:
        _ecoa_model : The ECOA model.
    """

    _ecoa_model = None

    def __init__(self, ecoa_model):
        self._ecoa_model = ecoa_model

    def compute(self) -> None:
        """Checks the language of each parsed module implementation."""
        for key, module_impl in self._ecoa_model.module_impls.items():
            component_impl_name = key.split(":")[0]
            if module_impl.language.lower() not in ["c", "c++"]:
                raise ValueError(
                    f"Unsupported implementation language {module_impl.language} for module "
                    + f"{component_impl_name}:{module_impl.name}"
                )
