class IgnoreModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    name: str