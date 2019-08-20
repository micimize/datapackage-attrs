import typing as t

import attr
from typing_extensions import Literal

converted = parse_keys(my_dict, type="camel")


FieldTypes = Literal[
    "any",
    "array",
    "boolean",
    "date",
    "datetime",
    "duration",
    "geojson",
    "geopoint",
    "integer",
    "number",
    "object",
    "string",
    "time",
    "year",
    "yearmonth",
]


@attr.s(auto_attribs=True)
class Field:
    """ """

    name: str
    title: str = None
    type: FieldTypes = "any"
    format: str = None
    description: str = None
    constraints: dict = None
    rdf_type: str = None


@attr.s(auto_attribs=True)
class TableSchema:
    """ """

    name: str
    title: str = None
    type: FieldTypes = "any"
    format: str = None
    description: str = None
    constraints: dict = None
    rdf_type: str = None
