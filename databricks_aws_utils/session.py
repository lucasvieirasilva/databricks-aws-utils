"""A helper to help getting a Boto3 session"""
from typing import Optional

import boto3
from boto3.session import Session


def get_session(
    region: str = "us-east-1",
    profile: Optional[str] = None,
    role: Optional[str] = None,
    context: Optional[str] = None,
) -> Session:
    """
        AWS Boto3 session creator

        Args:
            region (`str`): the AWS Region, default us-east-1
            profile (`str`, optional): the AWS Profile to be used
            role (`str`, optional): the AWS Role to be assumed (Required if profile is not defined)
            context (`str`, optional): the Role Session Name to be used when assuming role \
                (Required if profile is not defined)
        Returns:
            `Session` boto3 session object
    """
    if profile is not None:
        return boto3.Session(
            profile_name=profile,
            region_name=region
        )

    session = boto3.Session(region_name=region)

    if role is not None and context is not None:
        sts_client = session.client('sts')
        response = sts_client.assume_role(
            RoleArn=role,
            RoleSessionName=context
        )

        credentials = response['Credentials']
        return boto3.Session(
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    return session
