import typing as t

import attr
from tableschema import Field, Schema

from _types import TypeInfo, type_map


def make_attr_ib(field: Field):
    field_type_info: TypeInfo = type_map.get(field.type, TypeInfo(t.Any))
    validators = []
    if field_type_info.py_type != t.Any:
        instance_of = attr.validators.instance_of(field_type_info.py_type)
        if not field.required:
            instance_of = attr.validators.optional(instance_of)
        validators.append(instance_of)
    return (
        field.name,
        attr.ib(
            type=field_type_info.py_type,
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
