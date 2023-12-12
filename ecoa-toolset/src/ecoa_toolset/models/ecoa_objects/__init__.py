# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The ecoa_object module."""

from .ecoa_bin_desc_2_0 import BinaryDependency, BinaryModule, BinDesc, ProcessorTarget
from .ecoa_common_2_0 import ProgrammingLanguage, Use
from .ecoa_cross_platforms_view_2_0 import Composite, EuidsBinding, View, WireMapping
from .ecoa_deployment_2_0 import (
    ComponentLog,
    ComputingNodeConfiguration,
    Deployment,
    LogPolicy,
    ModuleLog,
    PlatformConfiguration,
    PlatformMessages,
    ProtectionDomain,
    WireMapping,
)
from .ecoa_implementation_2_0 import (
    ComponentImplementation,
    DataLink,
    DynamicTriggerInstance,
    Event,
    EventLink,
    Instance,
    ModuleImplementation,
    ModuleInstance,
    ModuleType,
    OpRef,
    OpRefActivatable,
    OpRefActivatableFifo,
    OpRefActivatingFifo,
    OpRefExternal,
    OpRefTrigger,
    Parameter,
    PinfoValue,
    PrivatePinfo,
    PropertyValue,
    PropertyValues,
    PublicPinfo,
    RequestLink,
    RequestResponse,
    ServiceQoS,
    TriggerInstance,
    VersionedData,
)
from .ecoa_interface_2_0 import Data, EEventDirection, Event, Operations, Parameter, RequestResponse, ServiceDefinition
from .ecoa_interface_qos_2_0 import Data, Event, OperationRate, Operations, RequestResponse, ServiceInstanceQoS
from .ecoa_logicalsystem_2_0 import (
    LogicalComputingNodeLinks,
    LogicalComputingPlatform,
    LogicalComputingPlatformLinks,
    LogicalSystem,
)
from .ecoa_project_2_0 import Ecoaproject, EcoaProject, EliEuids, Files
from .ecoa_types_2_0 import (
    Array,
    Constant,
    DataTypes,
    EBasic,
    Enum,
    EnumValue,
    Field,
    FixedArray,
    Library,
    Record,
    Simple,
    Union,
    VariantRecord,
)
from .ecoa_uid_2_0 import Id, IdMap
