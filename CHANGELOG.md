# CHANGELOG



## v1.5.0 (2023-09-06)

### Ci

* ci: add semantic release (#3) ([`bc0c135`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/bc0c1353eef8ee7dd25416bf927fc23f734d130f))

### Documentation

* docs: remove readthedocs files and update readme to add usage guidance (#4) ([`2154a7f`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/2154a7ff9c13f23ae004e8e583c93f61e50847ab))

### Feature

* feat: add python 3.11 support (#5) ([`ef340b6`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/ef340b68e3105bbb002fa544fe62b377e8ce9a7a))


## v1.4.0 (2023-08-07)

### Unknown

* Added support for Python 3.10 ([`1af1989`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/1af19891eabcfe9b483d5d92651ac0ad12703988))


## v1.3.3 (2023-07-25)

### Unknown

* Fix `DeltaTableUtils.schema_to_glue` to check if the column data type is truncated in the spark list columns function and use the Spark SQL to get the column data type ([`04a53da`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/04a53daeb9209ac3b2422d5a41b7a8c643b432cf))


## v1.3.2 (2023-05-22)

### Unknown

* Fix `DeltaTableUtils.to_athena_v3` to set root parameters instead of `SerdeInfo` parameters ([`98d4a09`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/98d4a09bc094f82655e72c3ac18867c7204fbaf0))

* Fix `DeltaTableUtils.to_athena_v3` to set storage descriptor parameters instead of `SerdeInfo` parameters ([`4e1f7c5`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/4e1f7c592f0c0affe076815cdee20c455cb3c55e))


## v1.3.1 (2023-05-22)

### Unknown

* Fix `DeltaTableUtils.to_athena_v3` to use the Glue Table `SerdeInfo` correctly ([`d39afa7`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/d39afa72de39b9988b04bb68be62456fec3dbf85))

* upgrade readthedocs requirements ([`4d915e4`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/4d915e4fc1b8c3ba01331c98d8cfeefb82b3e9c7))


## v1.3.0 (2023-05-22)

### Unknown

* rollback github actions python version ([`41c57fd`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/41c57fdd51e8c42a5dc0283b39f8002e772f87d8))

* Changed `DeltaTableUtils` to add `to_athena_v3` method ([`47c3ed6`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/47c3ed665a20e83035f3d2e283b4af71e83674ea))


## v1.2.1 (2023-03-22)

### Unknown

* Fix `DeltaTableUtils` when the table has partition columns. ([`82c1e83`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/82c1e83043b378e8dee61d0ea9bbae2e9d14128d))

* update poetry.lock ([`a32b759`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/a32b759af0684c71f1fd29a7b1b119d773fde0b5))


## v1.2.0 (2023-03-22)

### Unknown

* fix publish workflow ([`ee85075`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/ee85075bd74767930e62f2cf702718ccb054c77e))

* Changed `DeltaTableUtils` to use spark catalog list columns instead `DESCRIBE TABLE` sql. (#2) ([`0461072`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/0461072661c1fbceccbe3c499bd859cda4a60354))


## v1.1.1 (2022-02-16)

### Unknown

* Bump version to `1.1.1` ([`8e03db0`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/8e03db0145d6401cbf4b0719332952dfe2abb564))

* Merge pull request #1 from lucasvieirasilva/issue-1

Fix `DeltaTableUtils` when the table has partition columns. ([`15d44c3`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/15d44c30daeb0198118c0a85483d1a9fa969fb75))

* Fix `DeltaTableUtils` when the table has partition columns. ([`c4a44f1`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/c4a44f1a8f7a755a0b3200789b52658eb777b921))


## v1.1.0 (2022-01-25)

### Unknown

* Release 1.1.0v ([`c11620a`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/c11620adb9e3c4d91c78aec2bf795a8a10175737))

* Add python 3.9 support ([`90744fe`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/90744fe8a129e2f14dd5a4692db10ab5a4cddb8a))


## v1.0.0 (2021-11-22)

### Unknown

* Update install docs ([`adcaa6b`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/adcaa6b3ba239b2ba847595563ab256e4c59395c))

* Add pydoc-markdown requirements ([`cd24399`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/cd24399ee1495f36d1cb4d8ea8bb934d09964a8a))

* Add initial project version ([`81c3070`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/81c30706cd1757dadec722662b172d850220c645))

* Initial commit ([`bb062a6`](https://github.com/lucasvieirasilva/databricks-aws-utils/commit/bb062a61a40d3fb0a35bb2e20df51e5da9e169ea))
