from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_FREE_RESTR_FIELDS = [
    ("record_id", 1, 2, "str"), # 08
    ("restriction_key", 3, 2, "int"),
    ("restriction_type", 5, 2, "str"),
    ("restriction_remark", 7, 70, "str"),
    ("restriction_flag", 77, 1, "str"),
    # Filler at 78 (len 10)
    # Tape filler 423 bytes at 88
    # Ignoring fillers.
]
