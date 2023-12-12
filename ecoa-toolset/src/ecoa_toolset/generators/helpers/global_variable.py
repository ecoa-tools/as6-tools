# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""GlobalVariableHelper class.
"""

# Standard library imports
from typing import Any

# Internal library imports
from ecoa_toolset.models.components import Variable
from ecoa_toolset.models.ecoa_objects import ecoa_types_2_0


class CMGlobalVariable(Variable):
    """The Container Mock Global Variable.

    Args:
        name: Variable's name
        namespace: Variable's namespace
        type: Variable's type
        type_category: Variable's type category
        language: The language
        value: Variable's default value
        is_out: True if the variable is an ouput, False otherwise
    """

    module_impl_name: str = None
    language: str = None
    value: str = None
    is_out: bool = None

    def __init__(
        self,
        name: str,
        namespace: str,
        type: str,
        type_category,
        module_impl_name: str,
        language: str,
        value: str,
        is_out: str = False,
    ):
        super().__init__(name, namespace, type, type_category)
        self.module_impl_name = module_impl_name
        self.language = language
        self.value = value
        self.is_out = is_out

    def accept(self, visitor, **kwargs) -> Any:
        return visitor.visit_CMGlobalVariable(self, **kwargs)


class CMGlobalVariableHelper:
    """"""

    _ecoa_model = None
    _global_variables = None

    def __init__(self, ecoa_model):
        self._ecoa_model = ecoa_model
        self._global_variables = {}
        self._build_global_variables()

    def _build_global_variables(self):
        data_read = [read for v in self._ecoa_model.data_read.values() for read in v]
        data_written = [written for v in self._ecoa_model.data_written.values() for written in v]
        request_send = [send for v in self._ecoa_model.requests_send.values() for send in v]

        self._add_global_vars_for_versioned_data(data_read, data_written)
        self._add_global_request_response_id(request_send)
        self._add_global_request_response_instance_id(request_send)
        self._add_global_request_response_out_parameter(request_send)

    def _add_global_vars_for_versioned_data(self, data_read, data_written) -> None:
        liste1 = []
        liste2 = []
        liste3 = []
        variable_name_first_list = []
        for i, vd in enumerate(data_read + data_written):
            module_impl = self._ecoa_model.module_impls.get(vd.component_impl_name + ":" + vd.module_impl_name)
            for key in vd.writers.keys() if i < len(data_read) else vd.readers.keys():
                module_inst_name, component_name, component_operation = tuple(key.split(":"))
                variable_name = module_inst_name + "_" + component_name + "__" + component_operation + "_data"
                variable_name_stamp = module_inst_name + "_" + component_name + "__" + component_operation + "_stamp"
                variable_name_first = (
                    module_inst_name + "_" + component_name + "__" + component_operation + "_first_write"
                )
                liste1.append(
                    CMGlobalVariable(
                        variable_name,
                        vd.type.split(":")[0],
                        vd.type.split(":")[1],
                        self._ecoa_model.types_helper.get_type_category(vd.type),
                        module_impl.name,
                        module_impl.language.lower(),
                        None,
                        is_out=True,
                    )
                )
                liste2.append(
                    CMGlobalVariable(
                        variable_name_stamp,
                        "ECOA",
                        "uint32",
                        ecoa_types_2_0.Simple,
                        module_impl.name,
                        module_impl.language.lower(),
                        "0",
                    )
                )
                if variable_name_first not in variable_name_first_list:
                    if i >= len(data_read):
                        liste3.append(
                            CMGlobalVariable(
                                variable_name_first,
                                "ECOA",
                                "boolean8",
                                ecoa_types_2_0.Simple,
                                module_impl.name,
                                module_impl.language.lower(),
                                "1",
                            )
                        )
                    variable_name_first_list.append(variable_name_first)
        self._global_variables["Versioned Data"] = liste1
        self._global_variables["Versioned Data Stamp"] = liste2
        self._global_variables["Versioned Data First Write"] = liste3

    def _add_global_request_response_id(self, request_send) -> None:
        variable_name_list = []
        liste = []
        for i, sender in enumerate(request_send):
            variable_name = sender.module_impl_name + "__" + sender.name + "_RR_ID"
            module_impl = self._ecoa_model.module_impls.get(sender.component_impl_name + ":" + sender.module_impl_name)
            if variable_name not in variable_name_list:
                liste.append(
                    CMGlobalVariable(
                        variable_name,
                        "ECOA",
                        "uint32",
                        ecoa_types_2_0.Simple,
                        module_impl.name,
                        module_impl.language.lower(),
                        str(i),
                    )
                )
                variable_name_list.append(variable_name)
        self._global_variables["Request Responses ID"] = liste

    def _add_global_request_response_instance_id(self, request_send) -> None:
        variable_name_list = []
        liste = []
        for sender in request_send:
            variable_name = sender.module_impl_name + "__" + sender.name + "_RRI_ID"
            module_impl = self._ecoa_model.module_impls.get(sender.component_impl_name + ":" + sender.module_impl_name)
            if variable_name not in variable_name_list:
                liste.append(
                    CMGlobalVariable(
                        variable_name,
                        "ECOA",
                        "uint32",
                        ecoa_types_2_0.Simple,
                        module_impl.name,
                        module_impl.language.lower(),
                        "0",
                    )
                )
                variable_name_list.append(variable_name)
        self._global_variables["Request Responses Instance ID"] = liste

    def _add_global_request_response_out_parameter(self, request_send) -> None:
        variable_name_list = []
        liste = []
        for sender in request_send:
            for parameter in sender.outputs:
                variable_name = sender.module_impl_name + "__" + sender.name + "_" + parameter.name
                module_impl = self._ecoa_model.module_impls.get(
                    sender.component_impl_name + ":" + sender.module_impl_name
                )
                if variable_name not in variable_name_list:
                    liste.append(
                        CMGlobalVariable(
                            variable_name,
                            parameter.namespace,
                            parameter.type,
                            parameter.type_category,
                            module_impl.name,
                            module_impl.language.lower(),
                            "0",
                            is_out=True,
                        )
                    )
                    variable_name_list.append(variable_name)
        self._global_variables["Request Responses Out Parameters"] = liste

    def find_all(self, module_impl_name: str = None):
        filtered = self._global_variables
        if module_impl_name is not None:
            tmp = {}
            for k, v in filtered.items():
                liste = [gv for gv in v if gv.module_impl_name == module_impl_name]
                if liste:
                    tmp[k] = liste
            filtered = tmp
        return filtered
