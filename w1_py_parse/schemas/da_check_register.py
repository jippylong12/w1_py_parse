from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_CHECK_REGISTER_FIELDS = [
    ("record_id", 1, 2, "str"), # 13
    ("register_date_century", 3, 2, "int"),
    ("register_date_year", 5, 2, "int"),
    ("register_date_month", 7, 2, "int"),
    ("register_date_day", 9, 2, "int"),
    ("register_number", 11, 8, "int"),
    # Filler at 19 (len 10)
    # Tape filler 482 bytes at 29
    # Ignoring fillers.
]
