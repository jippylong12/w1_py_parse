from .da_root import DA_ROOT_FIELDS
from .da_permit import DA_PERMIT_FIELDS
from .da_field import DA_FIELD_FIELDS
from .da_field_specific import DA_FIELD_SPECIFIC_FIELDS
from .da_field_bhl import DA_FIELD_BHL_FIELDS
from .da_can_restr import DA_CAN_RESTR_FIELDS
from .da_can_restr_field import DA_CAN_RESTR_FIELD_FIELDS
from .da_free_restr import DA_FREE_RESTR_FIELDS
from .da_free_restr_field import DA_FREE_RESTR_FIELD_FIELDS

SCHEMA_ID_TO_NAME = {
    "01": "DAROOT",
    "02": "DAPERMIT",
    "03": "DAFIELD",
    "04": "DAFLDSPC",
    "05": "DAFLDBHL",
    "06": "DACANRES",
    "07": "DACANFLD",
    "08": "DAFRERES",
    "09": "DAFREFLD",
    "10": "DAPMTBHL",
    "11": "DAALTADD",
    "12": "DAREMARK",
    "13": "DACHECK",
    "14": "DAW999A1",
    "15": "DAW999B1",
}

SCHEMA_NAME_TO_ID = {v: k for k, v in SCHEMA_ID_TO_NAME.items()}

# Registry of implemented schemas
SCHEMA_FIELDS = {
    "01": DA_ROOT_FIELDS,
    "02": DA_PERMIT_FIELDS,
    "03": DA_FIELD_FIELDS,
    "04": DA_FIELD_SPECIFIC_FIELDS,
    "05": DA_FIELD_BHL_FIELDS,
    "06": DA_CAN_RESTR_FIELDS,
    "07": DA_CAN_RESTR_FIELD_FIELDS,
    "08": DA_FREE_RESTR_FIELDS,
    "09": DA_FREE_RESTR_FIELD_FIELDS,
}
