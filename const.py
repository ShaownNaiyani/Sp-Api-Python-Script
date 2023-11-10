import os
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN = os.environ["refresh_token"]
LWA_APP_ID = os.environ["lwa_app_id"]
CLIENT_SECRET = os.environ["lwa_client_secret"]
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
ROLE_ARN = os.environ["role_arn"]
