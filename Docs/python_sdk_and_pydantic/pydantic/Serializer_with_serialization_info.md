@field_serializer('field_name')
def serialize_field(self, value: Any, info: FieldSerializationInfo) -> Any:
    return transformed_value