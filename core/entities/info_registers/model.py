from core.orm.base_model import BaseModel


__all__ = ["InfoRegister", "InfoRegisterResult"]


class InfoRegister(BaseModel):
    class Meta:
        abstract = True


class InfoRegisterResult(BaseModel):
    class Meta:
        abstract = True
