# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses import field as field2
from enum import Enum
from typing import List, Optional

from ecoa_toolset.models.ecoa_objects.ecoa_common_2_0 import Use

__NAMESPACE__ = "http://www.ecoa.technology/types-2.0"


@dataclass
class Array:
    """Variable-size (bounded capacity) array.

    :ivar item_type:
    :ivar max_number:
    :ivar name:
    :ivar comment:
    """

    item_type: Optional[str] = field2(default=None, metadata=dict(name="itemType", type="Attribute", required=True))
    max_number: Optional[str] = field2(
        default=None,
        metadata=dict(
            name="maxNumber",
            type="Attribute",
            required=True,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%|[0-9]+",
        ),
    )
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=True, metadata={"type": "Ignore"})


@dataclass
class Constant:
    """Constant definition.

    :ivar name:
    :ivar type:
    :ivar value:
    :ivar comment:
    """

    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    value: Optional[str] = field2(
        default=None,
        metadata=dict(
            type="Attribute",
            required=True,
            length=1,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%",
        ),
    )
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=False, metadata={"type": "Ignore"})


class EBasic(Enum):
    """ECOA basic types.

    :cvar BOOLEAN8:
    :cvar INT8:
    :cvar INT16:
    :cvar INT32:
    :cvar INT64:
    :cvar UINT8:
    :cvar UINT16:
    :cvar UINT32:
    :cvar UINT64:
    :cvar CHAR8:
    :cvar BYTE:
    :cvar FLOAT32:
    :cvar DOUBLE64:
    """

    BOOLEAN8 = "boolean8"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    CHAR8 = "char8"
    BYTE = "byte"
    FLOAT32 = "float32"
    DOUBLE64 = "double64"


@dataclass
class EnumValue:
    """A possible value of an enumerated type.

    :ivar name:
    :ivar valnum:
    :ivar comment:
    """

    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    valnum: Optional[str] = field2(
        default=None,
        metadata=dict(
            type="Attribute",
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%|(\+|-)?[0-9]*",
        ),
    )
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))


@dataclass
class Field:
    """
    :ivar name:
    :ivar type:
    :ivar comment:
    """

    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))


@dataclass
class FixedArray:
    """Fixed-size array (size is always equal to max capacity)

    :ivar item_type:
    :ivar max_number:
    :ivar name:
    :ivar comment:
    """

    item_type: Optional[str] = field2(default=None, metadata=dict(name="itemType", type="Attribute", required=True))
    max_number: Optional[str] = field2(
        default=None,
        metadata=dict(
            name="maxNumber",
            type="Attribute",
            required=True,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%|[0-9]+",
        ),
    )
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=True, metadata={"type": "Ignore"})


@dataclass
class Simple:
    """A type based on a predefined type (simple or E_basic) with a name, min/max
    constraints, and a unit.

    :ivar type:
    :ivar name:
    :ivar min_range:
    :ivar max_range:
    :ivar unit: Use of International System units is
              recommended.
    :ivar precision: Precision of values
    :ivar comment:
    """

    type: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    min_range: Optional[str] = field2(
        default=None,
        metadata=dict(
            name="minRange",
            type="Attribute",
            length=1,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%",
        ),
    )
    max_range: Optional[str] = field2(
        default=None,
        metadata=dict(
            name="maxRange",
            type="Attribute",
            length=1,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%",
        ),
    )
    unit: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    precision: Optional[str] = field2(
        default=None,
        metadata=dict(
            type="Attribute",
            length=1,
            pattern=r"%([A-Za-z][A-Za-z0-9_\.]*:)?[A-Za-z][A-Za-z0-9_]*%",
        ),
    )
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=False, metadata={"type": "Ignore"})


@dataclass
class Union:
    """
    :ivar name:
    :ivar type:
    :ivar when:
    :ivar comment:
    """

    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    when: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=True, metadata={"type": "Ignore"})


@dataclass
class Enum:
    """Enumerated type.

    :ivar value:
    :ivar name:
    :ivar type:
    :ivar comment:
    """

    value: List[EnumValue] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    type: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=False, metadata={"type": "Ignore"})


@dataclass
class Record:
    """A record with named fields (Ada record, C struct)

    :ivar field:
    :ivar name:
    :ivar comment:
    """

    field: List[Field] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=True, metadata={"type": "Ignore"})


@dataclass
class VariantRecord:
    """A record with variable parts: each "union" exists only if the selector has
    the value given by the "when" attribute.

    :ivar field:
    :ivar union:
    :ivar name:
    :ivar select_name:
    :ivar select_type:
    :ivar comment:
    """

    field: List[Field] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    union: List[Union] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=1,
            max_occurs=9223372036854775807,
        ),
    )
    name: Optional[str] = field2(default=None, metadata=dict(type="Attribute", required=True))
    select_name: Optional[str] = field2(default=None, metadata=dict(name="selectName", type="Attribute", required=True))
    select_type: Optional[str] = field2(default=None, metadata=dict(name="selectType", type="Attribute", required=True))
    comment: Optional[str] = field2(default=None, metadata=dict(type="Attribute"))
    is_complex: Optional[bool] = field2(default=True, metadata={"type": "Ignore"})


@dataclass
class DataTypes:
    """A set of data type definitions.

    :ivar simple:
    :ivar record:
    :ivar constant:
    :ivar variant_record:
    :ivar array:
    :ivar fixed_array:
    :ivar enum:
    """

    simple: List[Simple] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    record: List[Record] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    constant: List[Constant] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    variant_record: List[VariantRecord] = field2(
        default_factory=list,
        metadata=dict(
            name="variantRecord",
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    array: List[Array] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    fixed_array: List[FixedArray] = field2(
        default_factory=list,
        metadata=dict(
            name="fixedArray",
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    enum: List[Enum] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )


@dataclass
class Library:
    """A set of data types in a library.

    :ivar use:
    :ivar types:
    """

    use: List[Use] = field2(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            min_occurs=0,
            max_occurs=9223372036854775807,
        ),
    )
    types: Optional[DataTypes] = field2(
        default=None,
        metadata=dict(
            type="Element",
            namespace="http://www.ecoa.technology/types-2.0",
            required=True,
        ),
    )


@dataclass
class Library(Library):
    class Meta:
        name = "library"
        namespace = "http://www.ecoa.technology/types-2.0"
