import json
from typing import Dict, Optional

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from databricks_aws_utils import DatabrickAWSUtils


class RdsUtils(DatabrickAWSUtils):
    """
        AWS RDS Integration Utils.

        Using `pg8000` in the Databricks notebook not works properly, so, AWS Data Wrangler not work as well,
            then this module helps to abstract call to execute queries against to RDS using Spark Session
                using AWS Secrets manage to retrive the RDS instance authentication

        Args:
            spark (`SparkSession`): spark session
            secret_id (`str`): AWS Secrets Manager Secret Id
            aws_region (`str`, optional): AWS region, default `us-east-1`
            iam_role (`str`, optional): IAM Role ARN, if specified assumes the IAM role to perform the AWS API calls
            aws_access_key_id (`str`, optional): Temporary AWS Access Key Id
            aws_secret_access_key (`str`, optional): Temporary AWS Secret Access Key
            aws_session_token (`str`, optional): Temporary AWS Session Token

        Features:

        - Execute query against a database using Spark JDBC using AWS Secrets Manager
    """

    def __init__(
        self,
        spark: SparkSession,
        secret_id: str,
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
        self.secret_id = secret_id
        self.secret_data = self._get_secret(secret_id)

    def read_query(self, query: str, dbname: Optional[str] = None) -> DataFrame:
        """
            Run Query to the Database configured in the AWS Secrets Manager entry and returns the Spark DataFrame

            The AWS Secrets Manager entry needs to have these properties:

            - host
            - port
            - username
            - password
            - dbname
            - engine

            Example:

            ```json
            {
               "host": "myrds-dns",
               "post": 5432,
               "username": "myuser",
               "password": "mysecretpassword",
               "dbname": "mydatabase",
               "engine": "postgresql",
            }
            ```

            Args:
                query (`str`): SQL Query
                dbname (`str`, optional): Override the AWS Secret Manager DB Name

            Returns:
                `DataFrame`: Spark DataFrame
        """

        return self.spark.read.format("jdbc") \
            .option("url", self._get_url(self.secret_data, dbname)) \
            .option("dbtable", query) \
            .option("user", self.secret_data['username']) \
            .option("password", self.secret_data['password']) \
            .load()

    def _get_secret(self, secret_id: str) -> Dict[str, str]:
        """
            Retrive the secret data from the AWS Secrets Manager entry

            Args:
                secret_id (`str`): Secret Id

            Returns:
                `Dict[str, str]`: Secret data
        """
        client = self.session.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_id)
        return json.loads(response['SecretString'])

    def _get_url(self, secret_data: Dict[str, str], dbname: Optional[str] = None) -> str:
        """
            Generate JDBC URL based on the AWS Secret Manager data

            Args:
                secret_data (`Dict[str, str]`): Secret data
                dbname (`str`, optional): Override the AWS Secret Manager DB Name

            Returns:
                `str` JDBC URL
        """
        engine = secret_data['engine']
        host = secret_data['host']
        port = secret_data['port']

        if dbname:
            db_name = dbname
        else:
            db_name = secret_data['dbname']

        return f"jdbc:{engine}://{host}:{port}/{db_name}"
