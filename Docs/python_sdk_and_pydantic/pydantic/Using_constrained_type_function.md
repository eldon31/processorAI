from pydantic import BaseModel, conint

class Model(BaseModel):
    value: conint(gt=0, lt=100)