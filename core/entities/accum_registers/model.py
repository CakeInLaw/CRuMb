from datetime import datetime

from core.orm.base_model import BaseModel
from core.orm import fields as orm_fields


__all__ = ["AccumRegister", "AccumRegisterResult"]


class AccumRegister(BaseModel):
    id: int = orm_fields.BigIntField(pk=True)
    registrator: str = orm_fields.CharField(max_length=20)
    dt: datetime = orm_fields.DatetimeField()

    class Meta:
        abstract = True


class AccumRegisterResult(BaseModel):
    dt: datetime = orm_fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
