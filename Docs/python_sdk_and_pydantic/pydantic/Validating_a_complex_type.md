list_int_adapter = TypeAdapter(list[int])
validated_list = list_int_adapter.validate_python(["1", "2", "3"])  # Returns [1, 2, 3]