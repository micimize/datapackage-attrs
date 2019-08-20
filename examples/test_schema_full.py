import attr as attr
import typing as t

from decimal import Decimal
from datetime import time, date


@attr.s(auto_attribs=True, slots=True)
class TestSchemaFull:
    """A type generated from a full test schema

    A test type with all base table schema types.
    Has a particularly long docstring


    Attributes:
        first_name: The first name of the person
        last_name: The last name of the person
        gender: The gender of the person.
        age: The age of this person.
        period_employed: The period of employment, in years (eg: 2.6 Y).
        employment_start: The date this person started employment.
        daily_start: Usual start time for this person.
        daily_end: Usual end time for this person.
        is_management: Is this person part of upper management.
        photo: A photo of this person.
        interests: Declared interests of this person (work-related).
        home_location: A geopoint for this person's home address.
        position_title: This person's position in the company.
        extra: Extra information about this person.
        notes: Add any relevant notes for HR.
    """

    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None
    gender: t.Optional[str] = None
    age: t.Optional[int] = None
    period_employed: t.Optional[Decimal] = None
    employment_start: t.Optional[date] = None
    daily_start: t.Optional[time] = None
    daily_end: t.Optional[time] = None
    is_management: t.Optional[bool] = None
    photo: t.Optional[str] = None
    interests: t.Optional[list] = None
    home_location: t.Optional[t.Any] = None
    position_title: t.Optional[str] = None
    extra: t.Optional[dict] = None
    notes: t.Optional[t.Any] = None
