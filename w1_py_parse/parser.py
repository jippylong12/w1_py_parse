from typing import List, Dict, Any, Union
from .schemas import SCHEMA_01_FIELDS
from .models import RRCRecord, Schema01Record
import json

class W1Parser:
    def __init__(self):
        self.records: List[RRCRecord] = []

    def parse_file(self, filepath: str) -> None:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                self.parse_line(line)

    def parse_line(self, line: str) -> None:
        if len(line) < 2:
            return
        
        record_id = line[0:2]
        
        if record_id == '01':
            record = self._parse_schema_01(line)
            self.records.append(record)
        # Add other schemas here as they are implemented (02-15)
        else:
             # Ideally we keep track of unparsed lines or generic records
             pass

    def _parse_schema_01(self, line: str) -> Schema01Record:
        data = {}
        for name, start, length, type_ in SCHEMA_01_FIELDS:
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
            
        return Schema01Record(**data)

    def to_json(self) -> str:
        return json.dumps([r.to_dict() for r in self.records], default=str, indent=2)
