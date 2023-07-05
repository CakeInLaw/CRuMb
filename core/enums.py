from enum import StrEnum


__all__ = ["FieldTypes"]


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
