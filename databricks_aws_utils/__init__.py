"""
Databricks AWS Utils module

This module abstracts some Databricks AWS integration.
"""


import logging
from typing import Optional

import boto3

from databricks_aws_utils.session import get_session


class DatabrickAWSUtils(object):
    """
        Databricks AWS Integration Utils base class

        This base class contains the boto3 session config and logger

        Args:
            aws_region (`str`, optional): AWS region, default `us-east-1`
            iam_role (`str`, optional): IAM Role ARN, if specified assumes the IAM role to perform the AWS API calls
            aws_access_key_id (`str`, optional): Temporary AWS Access Key Id
            aws_secret_access_key (`str`, optional): Temporary AWS Secret Access Key
            aws_session_token (`str`, optional): Temporary AWS Session Token

        If no args are passed to this class uses the default boto3 session

        Attributes:
            logger (`Logger`): logger instance
            session (`boto3.Session`): boto3 session
    """

    def __init__(
        self,
        aws_region: Optional[str] = "us-east-1",
        iam_role: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None
    ) -> None:
        super().__init__()

        self.logger = logging.getLogger()

        if iam_role:
            self.logger.info(f"Assuming Role {iam_role}")
            session = get_session(region=aws_region, role=iam_role, context="databricks-aws-utils-python-library")
        elif aws_access_key_id and aws_secret_access_key and aws_session_token:
            self.logger.info(f"Using Temporary credentials {iam_role}")
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=aws_region
            )
        else:
            session = boto3.Session(region_name=aws_region)

        self.session = session
