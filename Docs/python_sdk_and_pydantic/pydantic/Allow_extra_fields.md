class AllowModel(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str