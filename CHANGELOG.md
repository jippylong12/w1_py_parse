# Changelog

All notable changes to this project will be documented in this file.

## [0.5.1] - 2025-12-10

### Changed
- Removed `filler` and `tape_filler` fields from `DaFieldSpecificRecord` and `DaFieldBhlRecord` models and schemas to clean up output.

## [0.5.0] - 2025-12-10

### Added
- Support for Schema 05 (Segment 5 - DAFLDBHL) parsing.
- `DaFieldBhlRecord` model.
- `parser.py` logic to handle '05' records.

## [0.4.0] - 2025-12-10

### Added
- Support for Schema 04 (Segment 4 - DAFLDSPC) parsing.
- `DaFieldSpecificRecord` model.
- `parser.py` logic to handle '04' records.

## [0.3.0] - 2025-12-10

### Added
- Support for Schema 03 (Segment 3 - DAFIELD) parsing.
- `DaFieldRecord` model for Field Segment.
- `parser.py` logic to handle '03' records.
- Updated `README.md` with usage examples and publishing instructions.

## [0.2.3] - 2025-12-10

### Changed
- `W1Parser.parse_file` now stores `RRCRecord` objects within the group, instead of dictionaries.
- `W1RecordGroup.to_json()` and `W1Parser.to_json()` updated to handle object serialization recursively.
- `parser.records[i][segment_id]` now returns an object with attribute access (e.g., `.api_number`), which also supports `.to_json()`.

## [0.2.2] - 2025-12-10

### Added
- `W1RecordGroup` custom dictionary class.
- `.to_json()` method on parsed items (e.g., `parser.records[0].to_json()`).

## [0.2.1] - 2025-12-10

### Changed
- `W1Parser.parse_file` now returns `List[Dict[str, Any]]` instead of `None`.
- Output structure is now hierarchical, grouped by the Root Segment ('01').
- `to_json` output updated to match the new hierarchical structure.

## [0.2.0] - 2025-12-10

### Added
- Support for Schema 02 (Segment 2 - DAPERMIT) parsing.
- `DaPermitRecord` model for Permit Master Segment.
- Unit tests for Schema 02 using real data samples.

## [0.1.3] - 2025-12-10

### Changed
- Refactored `Schema01` to `DaRootRecord` to match official RRC naming.
- `W1Parser.parse_file` now accepts a `schemas` argument for filtering by name (e.g., 'DAROOT') or ID (e.g., '01').

### Added
- Schema registry with placeholders for all 15 RRC segments.

## [0.1.2] - 2025-12-10

### Added
- Publishing instructions to `README.md`.
- Clean build step to `README.md` build instructions.

## [0.1.1] - 2025-12-10

### Changed
- Renamed project from `rrc_parser` to `w1_py_parse`.
- Updated package metadata for PyPI publication.

### Added
- `LICENSE` file.

## [0.1.0] - 2025-12-10

### Added
- Initial release.
- Core `W1Parser` class for parsing Texas RRC W-1 schema 01 files.
