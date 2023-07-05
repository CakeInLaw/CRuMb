from dataclasses import dataclass, field
from typing import TypeVar, Any, TypedDict
from uuid import UUID

from tortoise import fields
from core.orm import fields as orm_fields

from core.orm.base_model import BaseModel
from .enums import FieldTypes
from .filters import Filter


MODEL = TypeVar('MODEL', bound=BaseModel)
PK = TypeVar('PK', int, str, UUID)
SORT = list[str]
FILTERS = list[Filter]
DATA = dict[str, Any]
FK_TYPE = fields.IntField | fields.SmallIntField | fields.BigIntField |\
          fields.UUIDField | orm_fields.CharField | fields.Field


class BackFKData(TypedDict, total=False):
    add: list[DATA]
    edit: list[DATA]
    remove: list[PK]


class M2MData(TypedDict, total=False):
    add: list[PK]
    remove: list[PK]


@dataclass
class SortedData:
    db_field: dict[str, Any]
    o2o: dict[str, DATA]
    o2o_pk: dict[str, int]
    fk: dict[str, DATA]
    fk_pk: dict[str, int]
    back_o2o: dict[str, DATA]
    back_fk: dict[str, BackFKData]
    m2m: dict[str, M2MData]


@dataclass
class RepositoryDescription:
    all: dict[str, FieldTypes] = field(default_factory=dict)
    db_field: dict[str, fields.Field] = field(default_factory=dict)
    o2o: dict[str, fields.relational.OneToOneFieldInstance] = field(default_factory=dict)
    o2o_pk: dict[str, FK_TYPE] = field(default_factory=dict)
    fk: dict[str, fields.relational.ForeignKeyFieldInstance] = field(default_factory=dict)
    fk_pk: dict[str, FK_TYPE] = field(default_factory=dict)
    back_o2o: dict[str, fields.relational.BackwardOneToOneRelation] = field(default_factory=dict)
    back_fk: dict[str, fields.relational.BackwardFKRelation] = field(default_factory=dict)
    m2m: dict[str, fields.relational.ManyToManyFieldInstance] = field(default_factory=dict)
