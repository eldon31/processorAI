@field_serializer('field_name')
def serialize_field(self, value: Any) -> Any:
    return transformed_value