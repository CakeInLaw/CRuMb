from enum import IntEnum, StrEnum


class NomenclatureTypes(StrEnum):
    EQUIPMENT = "E"
    HOZ = "H"
    INVENTORY = "I"
    RAWS = "R"
    PROVISION = "P"
    DISHES = "D"


class NomenclatureUnits(StrEnum):
    UNITS = "U"
    KILOGRAMS = "K"
    LITERS = "L"
    CENTIMETERS = "C"
    METERS = "M"


class OperationTypes(IntEnum):
    WRITE_OFF = 1
