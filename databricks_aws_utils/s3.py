from typing import Optional
from urllib.parse import urlparse

from databricks_aws_utils import DatabrickAWSUtils


class S3Utils(DatabrickAWSUtils):
    """
        AWS S3 Utils.

        spark.read.{csv,parquet,etc}("<path>") throws an exception when the path not exist in the S3 Bucket,
            this module checks the prefix and returns a boolean to avoid throwing exception in the Spark Job

        Args:
            aws_region (`str`, optional): AWS region, default `us-east-1`
            iam_role (`str`, optional): IAM Role ARN, if specified assumes the IAM role to perform the AWS API calls
            aws_access_key_id (`str`, optional): Temporary AWS Access Key Id
            aws_secret_access_key (`str`, optional): Temporary AWS Secret Access Key
            aws_session_token (`str`, optional): Temporary AWS Session Token
    """

    def __init__(
        self,
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

    def check_path(self, uri: str) -> bool:
        """
            Checks if the S3 URI exists in the S3 Bucket

            Example:

            ```python
            from databricks_aws_utils.s3 import S3Utils

            S3Utils().check_path("s3://bucket_name/folder")
            ```
            Output: `True`


            Args:
                uri (`str`): S3 URI

            Returns:
                `bool`: if the uri exists in the S3 bucket
        """

        client = self.session.client('s3')

        parsed_uri = urlparse(uri, allow_fragments=False)

        response = client.list_objects_v2(
            Bucket=parsed_uri.netloc,
            Prefix=parsed_uri.path[1:],
            MaxKeys=1
        )

        return len(response.get('Contents', [])) > 0
