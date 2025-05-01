from dotenv import load_dotenv
from os import getenv
from kink import di

def bootstrap():
    load_dotenv(override=True)
    di["DISCORD_TOKEN"] = getenv('DISCORD_TOKEN')
    if di["DISCORD_TOKEN"] is None:
        raise ValueError("DISCORD_TOKEN environment variable is not set")
    di["GOOGLE_GCP_PROJECT_ID"] = getenv('GOOGLE_GCP_PROJECT_ID')
    if di["GOOGLE_GCP_PROJECT_ID"] is None:
        raise ValueError("GOOGLE_GCP_PROJECT_ID environment variable is not set")
    di["GOOGLE_GCP_REGION"] = getenv('GOOGLE_GCP_REGION')
    if di["GOOGLE_GCP_REGION"] is None:
        raise ValueError("GOOGLE_GCP_REGION environment variable is not set")
