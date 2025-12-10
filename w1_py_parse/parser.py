from typing import List, Dict, Any, Union, Optional, Set
from .schemas import DA_ROOT_FIELDS, SCHEMA_ID_TO_NAME, SCHEMA_NAME_TO_ID
from .schemas.da_permit import DA_PERMIT_FIELDS
from .models import RRCRecord, DaRootRecord, DaPermitRecord, W1RecordGroup
import json

class W1Parser:
    def __init__(self):
        self.records: List[W1RecordGroup] = []

    def parse_file(self, filepath: str, schemas: Optional[List[Union[str, int]]] = None) -> List[W1RecordGroup]:
        """
        Parse a W1/RRC data file.
        
        Args:
            filepath: Path to the file.
            schemas: List of schema identifiers to parse. Can be IDs ('01', 1) or names ('DAROOT').
                     If None, defaults to parsing all known/supported schemas.
                     
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
                        self.records.append(current_record)
                    
                    # Parse 01
                    root_record = self._parse_da_root(line)
                    # Initialize new group with 01 data
                    current_record = W1RecordGroup()
                    current_record["01"] = root_record.to_dict()
                    
                else:
                    # Sub-segment
                    # We only process sub-segments if we have an active 01 record
                    if current_record is not None:
                        parsed_record = None
                        if record_id == '02':
                             parsed_record = self._parse_da_permit(line)
                        
                        # Add to current record if parsed
                        if parsed_record:
                            current_record[record_id] = parsed_record.to_dict()

            # End of file: append last record
            if current_record is not None:
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

    def to_json(self) -> str:
        # records is now List[Dict]
        return json.dumps(self.records, default=str, indent=2)
