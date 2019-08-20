import typing as t

import attr
from tableschema import Field


"""
TODO implement validator support

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

TODO pyproject.toml config
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
"""


@attr.s(auto_attribs=True)
class TypeInfo:
    """

    Attributes:
        schema_type: The tableschema field type name
        py_type: The python type name to generate
        source_module: What module the py_type is defined as, if any
        definition: typing-based type definition to use, if any
            will use `import typing as t`
    """

    schema_type: str
    py_type: str

    source_module: t.Optional[str] = None
    definition: t.Optional[t.Union[str, bool]] = None

    # validators: t.Optional[t.List[t.Any]] = None


any_type = TypeInfo(schema_type="any", py_type="t.Any", definition=True)

types = (
    # primitives
    TypeInfo(schema_type="string", py_type="str"),
    TypeInfo(schema_type="boolean", py_type="bool"),
    TypeInfo(schema_type="integer", py_type="int"),
    TypeInfo(schema_type="array", py_type="list"),
    TypeInfo(schema_type="object", py_type="dict"),
    TypeInfo(source_module="decimal", schema_type="number", py_type="Decimal"),
    #
    # datetime
    TypeInfo(source_module="datetime", schema_type="date", py_type="date"),
    TypeInfo(source_module="datetime", schema_type="datetime", py_type="datetime"),
    TypeInfo(source_module="datetime", schema_type="duration", py_type="timedelta"),
    TypeInfo(source_module="datetime", schema_type="time", py_type="time"),
    TypeInfo(
        source_module="datetime",
        schema_type="year",
        py_type="Year",
        definition='t.NewType("Year", int)',
    ),
    TypeInfo(
        schema_type="yearmonth", py_type="YearMonth", definition="t.Tuple[int, int]"
    ),
    #
    # geo
    # TypeInfo(schema_type="geojson", py_type="geojson"),
    # TypeInfo(schema_type="geojson", py_type="geopoint"),
)

type_map = {t.schema_type: t for t in types}


def get_type_info(field: Field) -> t.Tuple[TypeInfo, str]:
    info = type_map.get(field.type, any_type)
    return (
        info,
        f"{field.name}: "
        + (
            f"t.Optional[{info.py_type}] = None" if not field.required else info.py_type
        ),
    )
