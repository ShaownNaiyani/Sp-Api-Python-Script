import const
import boto3


def get_temp_credentials():
    sts_client = boto3.client("sts")
    role_arn = const.ROLE_ARN
    role_session_name = "sp-api"

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )

    credentials = response["Credentials"]
    
    return {
        "AccessKeyId": credentials["AccessKeyId"],
        "SecretAccessKey": credentials["SecretAccessKey"],
        "SessionToken": credentials["SessionToken"]
    }

try:
    temp_credentials = get_temp_credentials()
   # print(temp_credentials)
except Exception as e:
    print(f"Error: {e}")

