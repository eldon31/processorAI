@field_serializer('field_name', mode='wrap')
def serialize_field(self, value: Any, handler: SerializerFunctionWrapHandler) -> Any:
    return handler(transformed_value)