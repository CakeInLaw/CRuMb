from typing import Type

from tortoise import fields

from .enums import FieldTypes


field_instance_to_type: dict[Type[fields.Field], FieldTypes] = {
    fields.IntField:                   FieldTypes.INT,
    fields.SmallIntField:              FieldTypes.INT,
    fields.BigIntField:                FieldTypes.INT,
    fields.FloatField:                 FieldTypes.FLOAT,
    fields.CharField:                  FieldTypes.STR,
    fields.TextField:                  FieldTypes.TEXT,
    fields.BooleanField:               FieldTypes.BOOL,
    fields.data.CharEnumFieldInstance: FieldTypes.ENUM,
    fields.data.IntEnumFieldInstance:  FieldTypes.ENUM,
    fields.DateField:                  FieldTypes.DATE,
    fields.DatetimeField:              FieldTypes.DATETIME,
}
