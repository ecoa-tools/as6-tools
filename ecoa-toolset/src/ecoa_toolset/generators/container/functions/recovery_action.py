# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Recovery Action generation class.
"""

from typing import List, Tuple

from ecoa_toolset.generators.container.common import Common

# Internal library imports
from ecoa_toolset.generators.generic.function import FunctionGenerator


class RecoveryActionGenerator(FunctionGenerator):
    """"""

    visited: List = None

    def __init__(self, indent_level: int, indent_step: int, body: bool):
        super().__init__(indent_level, indent_step, body)
        self.visited = [False, False]

    def _generate_global_function(self, language: str) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "global_recovery_action ("
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", language)
            + "recovery_action_type recovery_action,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_id asset_id,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_type asset_type"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + ")"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "if (recovery_action > ECOA"
            + Common.switch_lang("__", "::", language)
            + "recovery_action_type"
            + Common.switch_lang("_", "::", language)
            + "CHANGE_DEPLOYMENT)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + 'printf ("The recovery action %d is not implemented by '
            + 'the infrastructure\\n", (ECOA'
            + Common.switch_lang("__", "::", language)
            + "uint32) recovery_action);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.switch_lang("_", "::", language)
            + "OPERATION_NOT_AVAILABLE;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (asset_type > ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_type"
            + Common.switch_lang("_", "::", language)
            + "DEPLOYMENT)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + 'printf ("The targeted asset type %d is not implemented by '
            + 'the infrastructure\\n", (ECOA'
            + Common.switch_lang("__", "::", language)
            + "uint32) asset_type);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.switch_lang("_", "::", language)
            + "OPERATION_NOT_AVAILABLE;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "if (recovery_action == ECOA"
            + Common.switch_lang("__", "::", language)
            + "recovery_action_type"
            + Common.switch_lang("_", "::", language)
            + "CHANGE_DEPLOYMENT"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: (self.indent_level + 4)]
            + "&& (asset_type == ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_type"
            + Common.switch_lang("_", "::", language)
            + "COMPONENT || asset_type == ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_type"
            + Common.switch_lang("_", "::", language)
            + "PROTECTION_DOMAIN"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: (self.indent_level + 8)]
            + "|| asset_type == ECOA"
            + Common.switch_lang("__", "::", language)
            + "asset_type"
            + Common.switch_lang("_", "::", language)
            + "NODE))"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "{"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level += self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + 'printf ("The recovery action %d is not permitted for the targeted asset type %d\\n"'
            + ", (ECOA"
            + Common.switch_lang("__", "::", language)
            + "uint32) recovery_action, (ECOA"
            + Common.switch_lang("__", "::", language)
            + "uint32) asset_type);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.switch_lang("_", "::", language)
            + "OPERATION_NOT_AVAILABLE;"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "}"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "const char *recovery_action_type_map[] = "
            + '{ "Shutdown", "Cold restart", "Warm restart", "Change deployment" };'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "const char *asset_type_map[] = "
            + '{ "component", "protection domain", "node", "platform", "service", "deployment" };'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + 'printf ("%s the %s of ID %d\\n", recovery_action_type_map[recovery_action], '
            + "asset_type_map[asset_type], asset_id);"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return ECOA"
            + Common.switch_lang("__", "::", language)
            + "return_status"
            + Common.switch_lang("_OK", "()", language)
            + ";"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + "}" + Common.LINE_BREAK[:2]
        return generation

    def _generate_prototype(self, element: Tuple) -> str:
        generation = (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element[1])
            + "return_status"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
        )
        generation += Common.switch_lang(
            element[0] + "_container__",
            element[0] + "::Container::" if self.body else "",
            element[1],
        )
        generation += "recovery_action (" + Common.LINE_BREAK[:1]
        self.indent_level += self.indent_step
        generation += Common.switch_lang(
            (
                Common.SPACE_INDENTATION[: self.indent_level]
                + element[0]
                + "__context * context,"
                + Common.LINE_BREAK[:1]
            ),
            "",
            element[1],
        )
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element[1])
            + "recovery_action_type recovery_action,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element[1])
            + "asset_id asset_id,"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "ECOA"
            + Common.switch_lang("__", "::", element[1])
            + "asset_type asset_type"
            + Common.LINE_BREAK[:1]
        )
        self.indent_level -= self.indent_step
        generation += Common.SPACE_INDENTATION[: self.indent_level] + ")"
        return generation

    def _generate_body(self, element: Tuple) -> str:
        generation = ""
        if element[1] == "c":
            generation += Common.SPACE_INDENTATION[: self.indent_level] + "(void) context;" + Common.LINE_BREAK[:1]
        generation += (
            Common.SPACE_INDENTATION[: self.indent_level]
            + 'printf ("Recovery action performed by '
            + element[0]
            + ' ...");'
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[: self.indent_level]
            + "return global_recovery_action (recovery_action, asset_id, asset_type);"
        )
        return generation

    def generate(self, element: Tuple) -> str:
        """"""
        generation = ""
        if self.body and not self.visited[element[1] == "c"]:
            generation += self._generate_global_function(element[1])
            self.visited[element[1] == "c"] = True
        generation += super().generate(element)
        return generation
