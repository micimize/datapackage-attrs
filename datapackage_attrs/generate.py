import typing as t
from textwrap import dedent

import attr
from tableschema import Field, Schema  # type: ignore

from ._types import TypeInfo, get_type_info
from .module_classes import ModuleSnippet, SchemaClassDefinition


def make_attr_ib(field: Field):
    info: t.Optional[TypeInfo] = type_map.get(field.type, None)
    validators = []
    if info:
        instance_of: t.Any = attr.validators.instance_of(info.py_type)
        if not field.required:
            instance_of = attr.validators.optional(instance_of)
        validators.append(instance_of)
    return (
        field.name,
        attr.ib(
            type=info.py_type if info else t.Any,
            validator=validators,
            default=attr.NOTHING if field.required else None,
        ),
    )


def generate_attrs(
    schema_name: str,
    schema_path: str,
    docstring: str = None,
    *,
    repr_ns=None,
    repr=True,
    cmp=True,
    hash=None,
    init=True,
    slots=True,  # slots on by default
    frozen=False,
    weakref_slot=True,
    kw_only=False,
    cache_hash=False,
):
    schema = Schema(schema_path)
    cls = attr.make_class(
        schema_name,
        dict(make_attr_ib(field) for field in schema.fields),
        repr_ns=repr_ns,
        repr=repr,
        cmp=cmp,
        hash=hash,
        init=init,
        slots=slots,
        frozen=frozen,
        weakref_slot=weakref_slot,
        kw_only=kw_only,
        cache_hash=cache_hash,
    )
    cls.__doc__ = docstring
    return cls
