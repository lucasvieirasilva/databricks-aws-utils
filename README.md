# Databricks AWS Utils

Databricks AWS Utils is a library to abstract Databricks integration with AWS Services

## Features

- Convert Delta Table to be consumed by AWS Athena with Schema evolution
- Run queries against AWS RDS using AWS Secrets Manager to retrieve the connection properties and returns as Spark DataFrame

## Install

`pip install databricks-aws-utils`

## Delta Table to AWS Athena

### Motivation

Currently, delta tables are only compatible with AWS Athena engine v3, however, even with the compatibility, there are some limitations regarding the schema evolution, where the schema is not fully or correctly synchronized with the AWS Glue catalog, causing problems when querying the table.

To solve this problem, we created this library to convert the delta table columns to be compatible with the AWS Glue catalog and update the table metadata, allowing the table to be queried correctly by AWS Athena.

### Usage

```python
from databricks_aws_utils.delta_table import DeltaTableUtils

...

DeltaTableUtils(spark, 'my_schema.my_table_name').to_athena_v3()
```

The `to_athena_v3` function uses the spark session to capture the current delta schema and update the glue table.

**NOTE**: This feature is only compatible with AWS Athena engine v3, and the Databricks cluster must have access to the AWS Glue catalog.

**NOTE**: This feature is not supported by Databricks Unity Catalog, since it does not allow queries from AWS Athena.

#### Custom IAM Role

If you need to use a custom IAM Role to update the AWS Glue table, you can pass the role name as a parameter to the `DeltaTableUtils` class.

```python
from databricks_aws_utils.delta_table import DeltaTableUtils

...

DeltaTableUtils(
    spark,
    'my_schema.my_table_name',
    iam_role='my_custom_iam_role'
).to_athena_v3()
```

**NOTE**: The Databricks cluster must have permission to assume the custom IAM Role.

### Athena Engine v2

AWS Athena engine v2 doesn't support delta tables, so, to query a delta table using AWS Athena engine v2, it's necessary to generate Hive Symlink from the delta table and point to a different table.

```python
from databricks_aws_utils.delta_table import DeltaTableUtils

...

DeltaTableUtils(spark, 'my_schema.my_table_name').to_athena('my_schema', 'my_symlink_table_name')
```

**NOTE**: The schema name provided in the `to_athena` doesn't need to be the same as the delta table schema.

## Contributing

- See our [Contributing Guide](CONTRIBUTING.md)

## Change Log

- See our [Change Log](CHANGELOG.md)
