import attr as attr
import typing as t

from datetime import datetime


@attr.s(auto_attribs=True, slots=True)
class TestSimpleSchema:
    """A type generated from a small test schema

    Attributes:
        id: The unique identifier for this entity
        title: 
        timestamp: 
    """

    id: int
    title: t.Optional[str] = None
    timestamp: t.Optional[datetime] = None
