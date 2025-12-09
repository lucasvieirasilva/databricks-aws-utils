import re
from typing import Any, Dict, List, Optional, Tuple

import botocore
from delta.tables import DeltaTable
from pyspark.sql.catalog import Column
from pyspark.sql.session import SparkSession

from databricks_aws_utils import DatabrickAWSUtils


class DeltaTableUtils(DatabrickAWSUtils):
    """
    Delta Table AWS Integration Utils.

    > This Delta Table integration only works if the Databricks use the AWS Glue as the Metastore

    Args:
        spark (`SparkSession`): spark session
        name: (`str`): delta table name, must contain the database (e.g. `<database>.<table>`)
        aws_region (`str`, optional): AWS region, default `us-east-1`
        iam_role (`str`, optional): IAM Role ARN, if specified assumes the IAM role to perform the AWS API calls
        aws_access_key_id (`str`, optional): Temporary AWS Access Key Id
        aws_secret_access_key (`str`, optional): Temporary AWS Secret Access Key
        aws_session_token (`str`, optional): Temporary AWS Session Token

    Features:

    - Convert Databricks delta table to AWS Glue Format using symlink_format_manifest to allow the AWS Athena
        or Presto to consume externally
    """

    def __init__(
        self,
        spark: SparkSession,
        name: str,
        aws_region: Optional[str] = "us-east-1",
        iam_role: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None
    ) -> None:
        super().__init__(
            aws_region=aws_region,
            iam_role=iam_role,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )

        self.spark = spark
        self.name = name

    def to_athena_v3(self) -> None:
        """
        Dec 19, 2022, AWS announced the Athena V3 engine now supports Delta Lake tables.

        https://aws.amazon.com/about-aws/whats-new/2022/12/athena-enhances-read-support-delta-lake-table-format/

        However, there are some gotchas and requirements in the integrations.

        - The table needs to have a table property called `table_type` with the value `DELTA`.
        - AWS Glue should synchronize the columns and partitions with the Glue Catalog, however, for some reason \
            the columns and partitions are not synchronized for all tables, so it is necessary to synchronize \
            the columns and partitions manually.

        This method adds the `table_type` property to the table and synchronize the columns and partitions.
        """
        db_name, table_name = self.name.split('.')
        columns, partitions = self.schema_to_glue()
        client = self.session.client('glue')
        response = client.get_table(
            DatabaseName=db_name,
            Name=table_name
        )

        table = response['Table']
        del table['CreateTime']
        del table['UpdateTime']
        del table['DatabaseName']
        del table['IsRegisteredWithLakeFormation']
        del table['CreatedBy']
        del table['VersionId']
        del table['CatalogId']
        del table['IsMultiDialectView']
        if 'IsMaterializedView' in table:
            del table['IsMaterializedView']

        params = table['Parameters'] or {}
        params['table_type'] = 'DELTA'

        table['Parameters'] = params
        table['StorageDescriptor']['Columns'] = columns
        table['PartitionKeys'] = partitions

        self.logger.info("Updating table")
        client.update_table(
            DatabaseName=db_name,
            TableInput=table
        )
        self.logger.info("Table successfully updated")

    def to_athena(self, target_database: str, target_table: str) -> None:
        """
        Converts a Delta table to external table using AWS Athena or Presto
            format using `symlink_format_manifest`

        Presto Integration full documentation:
        <https://docs.databricks.com/delta/presto-integration.html#limitations>

        Args:
            delta_table (`str`): delta table name
            target_database (`str`): external database name
            target_table (`str`): external table name
            target_table_description (`str`, optional): external table description
        """

        columns, partitions = self.schema_to_glue()
        location = self.get_location()

        table = DeltaTable.forName(self.spark, self.name)
        client = self.session.client('glue')

        try:
            self.logger.info("Generating Symlink Format Manifest")
            table.generate('symlink_format_manifest')
            self.logger.info("Symlink Format Manifest Successfully generated")
            response = client.get_table(
                DatabaseName=target_database,
                Name=target_table
            )

            table = response['Table']
            self._update_glue_table(table, columns, partitions, location)
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'EntityNotFoundException':
                self._create_glue_table(target_database, target_table, columns,
                                        partitions, location)
            else:
                raise error

        if len(partitions) > 0:
            self.logger.info("Partitions detected, recovering partitions")
            self.spark.catalog.recoverPartitions(f"{target_database}.{target_table}")

    def get_table_name(self) -> str:
        """
        Get delta table name without the database name

        Returns:
            `str`: table name
        """
        return self.name.split('.')[1]

    def get_database_name(self) -> str:
        """
        Get database name from the delta table

        Returns:
            `str`: database name
        """
        if '.' not in self.name:
            raise RuntimeError(f"Cannot extract database name from the delta table name '{self.name}'")

        return self.name.split('.')[0]

    def get_location(self) -> str:
        """
        Get delta table location

        Returns:
            `str`: delta table location
        """
        client = self.session.client('glue')

        response = client.get_table(
            DatabaseName=self.get_database_name(),
            Name=self.get_table_name()
        )

        return response['Table']['StorageDescriptor']['Location']

    def schema_to_glue(self) -> Tuple[List[dict], List[dict]]:
        """
        Extracts the delta table schema and returns in the AWS Glue Format

        Returns:
            `Tuple[List[dict], List[dict]]` columns and partitions
        """
        columns = []
        partitions = []
        self.logger.info("Extracting table schema...")
        delta_columns = self.spark.catalog.listColumns(self.name)

        for column in delta_columns:
            col = {
                'Name': column.name,
                'Type': self._get_column_data_type(column),
                'Comment': column.description or ''
            }
            if column.isPartition:
                partitions.append(col)
            else:
                columns.append(col)

        self.logger.debug(f"Columns: {columns}")
        self.logger.debug(f"Partitions: {partitions}")
        return columns, partitions

    def _get_column_data_type(self, column: Column) -> str:
        """
        Resolve the column data type.

        If the data type is truncated, the method uses the Spark SQL to extract the data type.

        Args:
            column (`Column`): column object

        Returns:
            `str`: column data type
        """
        data_type = column.dataType

        if self._is_data_type_truncated(data_type):
            self.logger.warning(f"Data type for the column '{column.name}' is truncated, " +
                                "using the Spark SQL to extract the data type")

            col_details = self.spark.sql(f"DESC TABLE FORMATTED {self.name} {column.name}").collect()

            row = next((row for row in col_details if row.info_name == "data_type"), None)

            if row:
                data_type = row.info_value
            else:
                data_type = 'string'
                self.logger.warning(f"Data type for the column '{column.name}' not found, using 'string'")

        return data_type

    def _is_data_type_truncated(self, value: str) -> bool:
        """
        Identify if the data type value returned by the spark.catalog.listColumns is truncated.

        Pattern: `2 more fields`

        Args:
            value (`str`): data type value

        Returns:
            `bool`: True if the data type is truncated, False otherwise
        """
        pattern = r'(\d+)\s+more\s+fields'
        matches = re.findall(pattern, value)
        return len(matches) > 0

    def _create_glue_table(
        self,
        database_name: str,
        table_name: str,
        columns: List[dict],
        partitions: List[dict],
        location: str,
    ) -> None:
        """
        Creates the AWS Glue Table

        Args:
            database_name (`str`): database name
            table_name (`str`): table name
            columns (`List[dict]`): schema columns
            partitions (`List[dict]`): partitions definition
            location (`str`): delta table location
            table_description (`str`, optional): table description
        """
        client = self.session.client('glue')
        self.logger.info(f"Creating table '{database_name}.{table_name}'")
        client.create_table(
            DatabaseName=database_name,
            TableInput=self._generate_glue_table_input(table_name, columns, partitions, location)
        )
        self.logger.info(f"Table '{database_name}.{table_name}' successfully created")

    def _update_glue_table(
        self,
        table: dict,
        columns: List[dict],
        partitions: List[dict],
        location: str,
    ):
        """
        Updates the AWS Glue Table

        Args:
            session (`Session`): boto3 session
            database_name (`str`): database name
            table (`dict`): AWS Glue GetTable operation response
            columns (`List[dict]`): schema columns
            partitions (`List[dict]`): partitions definition
            location (`str`): delta table location
        """
        client = self.session.client('glue')
        database_name = table['DatabaseName']
        table_name = table['Name']

        self.logger.info(f"Updating table '{database_name}.{table_name}'")
        client.update_table(
            DatabaseName=database_name,
            TableInput=self._generate_glue_table_input(table_name, columns, partitions, location)
        )
        self.logger.info(f"Table '{database_name}.{table_name}' successfully updated")

    def _generate_glue_table_input(
        self,
        table_name: str,
        columns: List[dict],
        partitions: List[dict],
        location: str
    ) -> Dict[str, Any]:
        """
        Builds the AWS Glue TableInput object.

        Args:
            table_name (`str`): table name
            columns (`List[dict]`): schema columns
            partitions (`List[dict]`): partitions definition
            location (`str`): delta table location

        Returns:
            `Dict[str, Any]`: AWS Glue TableInput object
        """
        return {
            'Name': table_name,
            'Description': '',
            'StorageDescriptor': {
                'Columns': columns,
                'Location': f'{location}/_symlink_format_manifest',
                'InputFormat': 'org.apache.hadoop.hive.ql.io.SymlinkTextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                'SerdeInfo': {
                    'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
                    'Parameters': {
                            'serialization.format': '1'
                    }
                },
                'StoredAsSubDirectories': False
            },
            'PartitionKeys': partitions,
            'TableType': 'EXTERNAL_TABLE',
            'Parameters': {
                'EXTERNAL': 'TRUE'
            }
        }
