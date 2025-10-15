from pydantic import parse_obj_as
data = parse_obj_as(list[int], ['1', '2', '3'])