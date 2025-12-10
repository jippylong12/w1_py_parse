# Changelog

All notable changes to this project will be documented in this file.

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
