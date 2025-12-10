from typing import List, Dict, Any, Union, Optional, Set
from .schemas import DA_ROOT_FIELDS, SCHEMA_ID_TO_NAME, SCHEMA_NAME_TO_ID
from .models import RRCRecord, DaRootRecord
import json

class W1Parser:
    def __init__(self):
        self.records: List[RRCRecord] = []

    def parse_file(self, filepath: str, schemas: Optional[List[Union[str, int]]] = None) -> None:
        """
        Parse a W1/RRC data file.
        
        Args:
            filepath: Path to the file.
            schemas: List of schema identifiers to parse. Can be IDs ('01', 1) or names ('DAROOT').
                     If None, defaults to parsing all known/supported schemas.
        """
        allowed_ids = self._normalize_schema_filter(schemas)
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                self.parse_line(line, allowed_ids)

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
        if len(line) < 2:
            return
        
        record_id = line[0:2]
        
        # Check filter
        if allowed_ids is not None and record_id not in allowed_ids:
            return
        
        if record_id == '01':
            record = self._parse_da_root(line)
            self.records.append(record)
        # Add other schemas here as they are implemented (02-15)
        else:
             # Ideally we keep track of unparsed lines or generic records
             pass

    def _parse_da_root(self, line: str) -> DaRootRecord:
        data = {}
        for name, start, length, type_ in DA_ROOT_FIELDS:
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
            
        return DaRootRecord(**data)

    def to_json(self) -> str:
        return json.dumps([r.to_dict() for r in self.records], default=str, indent=2)
