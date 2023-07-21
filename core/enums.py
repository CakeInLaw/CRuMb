from enum import StrEnum


__all__ = ["FieldTypes", "NotifyStatus"]


class FieldTypes(StrEnum):
    INT = 'int'
    FLOAT = 'float'
    STR = 'str'
    TEXT = 'text'
    BOOL = 'bool'
    ENUM = 'enum'
    DATE = 'date'
    DATETIME = 'datetime'
    O2O = 'o2o'
    O2O_PK = 'o2o_pk'
    FK = 'fk'
    FK_PK = 'fk_pk'
    BACK_O2O = 'back_o2o'
    BACK_FK = 'back_fk'
    M2M = 'm2m'
    HIDDEN = 'hidden'

    @classmethod
    def db_field_types(cls):
        return (
            cls.INT,
            cls.FLOAT,
            cls.STR,
            cls.TEXT,
            cls.BOOL,
            cls.ENUM,
            cls.DATE,
            cls.DATETIME,
        )

    @classmethod
    def numeric_types(cls):
        return (
            cls.INT,
            cls.FLOAT
        )

    @classmethod
    def relational(cls):
        return (
            cls.O2O,
            cls.O2O_PK,
            cls.FK,
            cls.FK_PK,
            cls.BACK_O2O,
            cls.BACK_FK,
            cls.M2M,
        )

    @classmethod
    def pk_relation(cls):
        return (
            cls.O2O_PK,
            cls.FK_PK
        )

    @classmethod
    def no_pk_relation(cls):
        return (
            cls.O2O,
            cls.FK,
            cls.BACK_O2O,
            cls.BACK_FK,
            cls.M2M,
        )

    @classmethod
    def single_relation(cls):
        return (
            cls.O2O,
            cls.O2O_PK,
            cls.FK,
            cls.FK_PK,
            cls.BACK_O2O,
        )

    @classmethod
    def multiple_relation(cls):
        return (
            cls.BACK_FK,
            cls.M2M,
        )


class NotifyStatus(StrEnum):
    INFO = 'info'
    SUCCESS = 'success'
    WARN = 'warn'
    ERROR = 'error'
