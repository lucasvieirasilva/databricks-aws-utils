# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [1.3.3] - 2023-07-25

### Fixed

- Fix `DeltaTableUtils.schema_to_glue` to check if the column data type is truncated in the spark list columns function and use the Spark SQL to get the column data type.

## [1.3.2] - 2023-05-22

### Fixed

- Fix `DeltaTableUtils.to_athena_v3` to set root parameters instead of `SerdeInfo` parameters.

## [1.3.1] - 2023-05-22

### Fixed

- Fix `DeltaTableUtils.to_athena_v3` to use the Glue Table `SerdeInfo` correctly.

## [1.3.0] - 2023-05-22

### Changed

- Changed `DeltaTableUtils` to add `to_athena_v3` method.

## [1.2.1] - 2023-03-22

### Fixed

- Fix `DeltaTableUtils` when the table has partition columns.

## [1.2.0] - 2023-03-22

### Changed

- Changed `DeltaTableUtils` to use spark catalog list columns instead `DESCRIBE TABLE` sql.

## [1.1.1] - 2022-02-15

### Fixed

- Fix `DeltaTableUtils` when the table has partition columns.

## [1.1.0] - 2022-01-24

### Changed

- Add python `3.9` support.

## [1.0.0] - 2021-11-22

### Added

- Add `DeltaTableUtils` feature.
- Add `RDSUtils` feature.
- Add `S3Utils` feature.
