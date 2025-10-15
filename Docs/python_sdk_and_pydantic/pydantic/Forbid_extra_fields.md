class ForbidModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str