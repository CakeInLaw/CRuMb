from core.orm.base_model import BaseModel


__all__ = ["AccumRegister", "AccumRegisterResult"]


class AccumRegister(BaseModel):
    class Meta:
        abstract = True


class AccumRegisterResult(BaseModel):
    class Meta:
        abstract = True
