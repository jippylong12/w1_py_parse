from typing import List, Dict, Any, Union, Optional, Set
from .schemas import DA_ROOT_FIELDS, SCHEMA_ID_TO_NAME, SCHEMA_NAME_TO_ID
from .schemas.da_permit import DA_PERMIT_FIELDS
from .schemas.da_field import DA_FIELD_FIELDS
from .schemas.da_field_specific import DA_FIELD_SPECIFIC_FIELDS
from .schemas.da_field_bhl import DA_FIELD_BHL_FIELDS
from .schemas.da_can_restr import DA_CAN_RESTR_FIELDS
from .schemas.da_can_restr_field import DA_CAN_RESTR_FIELD_FIELDS
from .schemas.da_free_restr import DA_FREE_RESTR_FIELDS
from .schemas.da_free_restr_field import DA_FREE_RESTR_FIELD_FIELDS
from .schemas.da_permit_bhl import DA_PERMIT_BHL_FIELDS
from .schemas.da_alternate_addr import DA_ALTERNATE_ADDR_FIELDS
from .schemas.da_remark import DA_REMARK_FIELDS
from .schemas.da_check_register import DA_CHECK_REGISTER_FIELDS
from .schemas.da_surface_loc import DA_SURFACE_LOC_FIELDS
from .schemas.da_bottom_hole_loc import DA_BOTTOM_HOLE_LOC_FIELDS
from .models import RRCRecord, DaRootRecord, DaPermitRecord, DaFieldRecord, DaFieldSpecificRecord, DaFieldBhlRecord, DaCanRestrRecord, DaCanRestrFieldRecord, DaFreeRestrRecord, DaFreeRestrFieldRecord, DaPermitBhlRecord, DaAlternateAddressRecord, DaRemarkRecord, DaCheckRegisterRecord, DaSurfaceLocationRecord, DaBottomHoleLocationRecord, W1RecordGroup
from .lookups import COUNTY_CODES, WELL_STATUS_CODES, TYPE_WELL_CODES, CANNED_RESTRICTIONS
import json

class W1Parser:
    def __init__(self):
        self.records: List[W1RecordGroup] = []

    def parse_file(self, filepath: str, schemas: Optional[List[Union[str, int]]] = None, transform_codes: bool = False) -> List[W1RecordGroup]:
        """
        Parse a W1/RRC data file.
        
        Args:
            filepath: Path to the file.
            schemas: List of schema identifiers to parse. Can be IDs ('01', 1) or names ('DAROOT').
                     If None, defaults to parsing all known/supported schemas.
            transform_codes: If True, replaces codes (e.g. County Code) with readable strings.
                     
        Returns:
            List[W1RecordGroup]: A list of grouped records. Use .to_json() on items.
        """
        allowed_ids = self._normalize_schema_filter(schemas)
        
        current_record: Optional[W1RecordGroup] = None
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                if len(line) < 2:
                    continue
                
                record_id = line[0:2]
                
                # Check filter
                if allowed_ids is not None and record_id not in allowed_ids:
                    continue
                
                if record_id == '01':
                    # Start of a new logical record
                    # If we were building one, save it
                    if current_record is not None:
                        if transform_codes:
                            self._transform_group(current_record)
                        self.records.append(current_record)
                    
                    # Parse 01
                    root_record = self._parse_da_root(line)
                    # Initialize new group with 01 data
                    current_record = W1RecordGroup()
                    current_record["01"] = root_record
                    
                else:
                    # Sub-segment
                    # We only process sub-segments if we have an active 01 record
                    if current_record is not None:
                        parsed_record = None
                        if record_id == '02':
                             parsed_record = self._parse_da_permit(line)
                        elif record_id == '03':
                             parsed_record = self._parse_da_field(line)
                        elif record_id == '04':
                             parsed_record = self._parse_da_field_specific(line)
                        elif record_id == '05':
                             parsed_record = self._parse_da_field_bhl(line)
                        elif record_id == '06':
                             parsed_record = self._parse_da_can_restr(line)
                             if parsed_record:
                                if '06' not in current_record:
                                    current_record['06'] = []
                                current_record['06'].append(parsed_record)
                                # Set to None so it doesn't get added by the generic logic below
                                parsed_record = None
                        elif record_id == '07':
                             parsed_record = self._parse_da_can_restr_field(line)
                             if parsed_record:
                                if '07' not in current_record:
                                    current_record['07'] = []
                                current_record['07'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '08':
                             parsed_record = self._parse_da_free_restr(line)
                             if parsed_record:
                                if '08' not in current_record:
                                    current_record['08'] = []
                                current_record['08'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '09':
                             parsed_record = self._parse_da_free_restr_field(line)
                             if parsed_record:
                                if '09' not in current_record:
                                    current_record['09'] = []
                                current_record['09'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '10':
                             parsed_record = self._parse_da_permit_bhl(line)
                        
                        elif record_id == '11':
                             parsed_record = self._parse_da_alternate_addr(line)
                             if parsed_record:
                                if '11' not in current_record:
                                    current_record['11'] = []
                                current_record['11'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '12':
                             parsed_record = self._parse_da_remark(line)
                             if parsed_record:
                                if '12' not in current_record:
                                    current_record['12'] = []
                                current_record['12'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '13':
                             parsed_record = self._parse_da_check_register(line)
                             if parsed_record:
                                if '13' not in current_record:
                                    current_record['13'] = []
                                current_record['13'].append(parsed_record)
                                parsed_record = None
                        elif record_id == '14':
                             parsed_record = self._parse_da_surface_loc(line)
                        elif record_id == '15':
                             parsed_record = self._parse_da_bottom_hole_loc(line)
                             if parsed_record:
                                if '15' not in current_record:
                                    current_record['15'] = []
                                current_record['15'].append(parsed_record)
                                parsed_record = None
                        
                        # Add to current record if parsed
                        if parsed_record:
                            current_record[record_id] = parsed_record

            # End of file: append last record
            if current_record is not None:
                if transform_codes:
                    self._transform_group(current_record)
                self.records.append(current_record)
                
        return self.records
    
    def _normalize_schema_filter(self, schemas: Optional[List[Union[str, int]]]) -> Optional[Set[str]]:
        if schemas is None:
            return None # All permitted
        
        allowed = set()
        for s in schemas:
            s_str = str(s)
            # Check if it's a name like "DAROOT"
            if s_str in SCHEMA_NAME_TO_ID:
                allowed.add(SCHEMA_NAME_TO_ID[s_str])
            # Check if it's an ID like "01"
            elif s_str in SCHEMA_ID_TO_NAME:
                allowed.add(s_str)
             # Check if it's an int/string ID like "1" -> "01"
            elif s_str.zfill(2) in SCHEMA_ID_TO_NAME:
                allowed.add(s_str.zfill(2))
            else:
                # Warning or ignore? For now ignore or assume raw ID if user knows what they are doing
                pass
        return allowed

    def parse_line(self, line: str, allowed_ids: Optional[Set[str]] = None) -> None:
        """
        Deprecated/Internal: parses a single line. 
        Note: This is stateless and doesn't support grouping on its own.
        """
        pass

    def _parse_da_root(self, line: str) -> DaRootRecord:
        data = self._extract_fields(line, DA_ROOT_FIELDS)
        return DaRootRecord(**data)

    def _parse_da_permit(self, line: str) -> DaPermitRecord:
        data = self._extract_fields(line, DA_PERMIT_FIELDS)
        return DaPermitRecord(**data)

    def _parse_da_field(self, line: str) -> DaFieldRecord:
        data = self._extract_fields(line, DA_FIELD_FIELDS)
        return DaFieldRecord(**data)

    def _parse_da_field_specific(self, line: str) -> DaFieldSpecificRecord:
        data = self._extract_fields(line, DA_FIELD_SPECIFIC_FIELDS)
        return DaFieldSpecificRecord(**data)

    def _parse_da_field_bhl(self, line: str) -> DaFieldBhlRecord:
        data = self._extract_fields(line, DA_FIELD_BHL_FIELDS)
        return DaFieldBhlRecord(**data)

    def _parse_da_can_restr(self, line: str) -> DaCanRestrRecord:
        data = self._extract_fields(line, DA_CAN_RESTR_FIELDS)
        return DaCanRestrRecord(**data)

    def _parse_da_can_restr_field(self, line: str) -> DaCanRestrFieldRecord:
        data = self._extract_fields(line, DA_CAN_RESTR_FIELD_FIELDS)
        return DaCanRestrFieldRecord(**data)

    def _parse_da_free_restr(self, line: str) -> DaFreeRestrRecord:
        data = self._extract_fields(line, DA_FREE_RESTR_FIELDS)
        return DaFreeRestrRecord(**data)

    def _parse_da_free_restr_field(self, line: str) -> DaFreeRestrFieldRecord:
        data = self._extract_fields(line, DA_FREE_RESTR_FIELD_FIELDS)
        return DaFreeRestrFieldRecord(**data)

    def _parse_da_permit_bhl(self, line: str) -> DaPermitBhlRecord:
        data = self._extract_fields(line, DA_PERMIT_BHL_FIELDS)
        return DaPermitBhlRecord(**data)

    def _parse_da_alternate_addr(self, line: str) -> DaAlternateAddressRecord:
        data = self._extract_fields(line, DA_ALTERNATE_ADDR_FIELDS)
        return DaAlternateAddressRecord(**data)

    def _parse_da_remark(self, line: str) -> DaRemarkRecord:
        data = self._extract_fields(line, DA_REMARK_FIELDS)
        return DaRemarkRecord(**data)

    def _parse_da_check_register(self, line: str) -> DaCheckRegisterRecord:
        data = self._extract_fields(line, DA_CHECK_REGISTER_FIELDS)
        return DaCheckRegisterRecord(**data)

    def _parse_da_surface_loc(self, line: str) -> DaSurfaceLocationRecord:
        data = self._extract_fields(line, DA_SURFACE_LOC_FIELDS)
        return DaSurfaceLocationRecord(**data)

    def _parse_da_bottom_hole_loc(self, line: str) -> DaBottomHoleLocationRecord:
        data = self._extract_fields(line, DA_BOTTOM_HOLE_LOC_FIELDS)
        return DaBottomHoleLocationRecord(**data)

    def _extract_fields(self, line: str, fields: List[Any]) -> Dict[str, Any]:
        data = {}
        for name, start, length, type_ in fields:
            # 1-based start index to 0-based
            idx = start - 1
            # Ensure line is long enough
            if idx >= len(line):
                # Field completely missing
                raw_val = ""
            else:
                raw_val = line[idx : idx + length]
            
            # Pad if short (e.g. line ends early)
            if len(raw_val) < length:
                raw_val = raw_val.ljust(length)
                
            val: Union[str, int] = raw_val
            
            if type_ == 'int':
                try:
                    val = int(raw_val)
                except ValueError:
                    val = 0 # Default to 0 if parsing fails or valid is spaces/empty
            else:
                # Str: strip? 
                # Preserving whitespace can be important for strict layouts, 
                # but typically for data usage we want trimmed strings.
                val = raw_val.strip()
                
            data[name] = val
        return data

    def _transform_group(self, group: W1RecordGroup) -> None:
        """
        Apply transformations to all records in a group.
        """
        for key, value in group.items():
            if isinstance(value, list):
                for item in value:
                     if isinstance(item, RRCRecord):
                        self._apply_transformations(item)
            elif isinstance(value, RRCRecord):
                 self._apply_transformations(value)

    def _apply_transformations(self, record: RRCRecord) -> None:
        """
        Apply lookup transformations to a single record.
        """
        if isinstance(record, DaRootRecord):
            if record.county_code in COUNTY_CODES:
                record.county_code = COUNTY_CODES[record.county_code]
                
        elif isinstance(record, DaPermitRecord):
            if record.county_code in COUNTY_CODES:
                record.county_code = COUNTY_CODES[record.county_code]
            if record.onshore_county in COUNTY_CODES:
                record.onshore_county = COUNTY_CODES[record.onshore_county]
            
            # Well Status
            if record.well_status in WELL_STATUS_CODES:
                record.well_status = WELL_STATUS_CODES[record.well_status]
                
            # Type Application (Type Well)
            if record.type_application in TYPE_WELL_CODES:
                record.type_application = TYPE_WELL_CODES[record.type_application]
                
        elif isinstance(record, DaCanRestrRecord):
            # Canned Restrictions
            if record.restriction_type in CANNED_RESTRICTIONS:
                # Often the restriction_type is just the code, but we might want to store the narrative alone
                # or replace the code? The user said "show the transformed data".
                # For restrictions, the narrative is the value. The code is just a key.
                # However, DaCanRestrRecord has 'restriction_type' (str) and 'restriction_remark' (str)?
                # Wait. In DaCanRestrRecord:
                # restriction_key (int)
                # restriction_type (str, length 2) -> matches "A ", "A1", "01" etc.
                # restriction_remark (str, length 35).
                # The manual says: "THESE CANNED RESTRICTIONS ARE PRINTED ON THE ACTUAL PERMIT... A 'Z' CANNED RESTRICTION INDICATES... FREE-FORM".
                # The narrative provided in the manual is very long (e.g. "REGULAR PROVIDED THIS WELL IS NEVER COMPLETED...").
                # Where does this narrative go?
                # DaCanRestrRecord has `restriction_remark` of length 35. That's likely for free-form or short args.
                # The Narrative itself might not fit in `restriction_remark`.
                # But the user asked to "show the transformed data".
                # Maybe I should replace `restriction_type` with the narrative?
                # But `restriction_type` is defined as str (length 2 in schema, but str in model).
                # If I replace it with a 200-char string, it fits in Python str.
                # It might be confusing if `restriction_type` becomes a long sentence.
                # But that's what "transformed data" implies.
                record.restriction_type = CANNED_RESTRICTIONS[record.restriction_type]


    def to_json(self) -> str:
        # records is now List[W1RecordGroup]
        def default_serializer(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            return str(obj)
        return json.dumps(self.records, default=default_serializer, indent=2)
