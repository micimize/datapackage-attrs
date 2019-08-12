import typing as t
from datetime import date, datetime, time, timedelta
from decimal import Decimal

import attr


@attr.s(auto_attribs=True)
class TypeInfo:
    py_type: type
    validators: t.Optional[t.List[t.Any]] = None


type_map: t.Dict[str, TypeInfo] = {
    "any": TypeInfo(py_type=t.Any),
    "array": TypeInfo(py_type=t.List[t.Any]),
    "boolean": TypeInfo(py_type=bool),
    "date": TypeInfo(py_type=date),
    "datetime": TypeInfo(py_type=datetime),
    "duration": TypeInfo(py_type=timedelta),
    "geojson": TypeInfo(py_type=t.Any),
    "geopoint": TypeInfo(py_type=t.Tuple[Decimal, Decimal]),
    "integer": TypeInfo(py_type=int),
    "number": TypeInfo(py_type=Decimal),
    "object": TypeInfo(py_type=dict),
    "string": TypeInfo(py_type=str),
    "time": TypeInfo(py_type=time),
    "year": TypeInfo(py_type=int),
    "yearmonth": TypeInfo(py_type=t.Tuple[int, int]),
}
