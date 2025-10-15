int_adapter = TypeAdapter(int)
validated_int = int_adapter.validate_python("123")  # Returns 123