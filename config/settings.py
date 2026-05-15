import os
from dotenv import load_dotenv

load_dotenv()

WEB_URL = os.getenv("WEB_URL")
TTCH_USERNAME = os.getenv("TTCH_USERNAME")
TTCH_PASSWORD = os.getenv("TTCH_PASSWORD")

WEEKLY_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1VELKyZUCr_THDbI8zBu_rAAOuIbvP-M344OWCTT4yRA/"
    "export?format=csv&gid=0"
)

CONFIG_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1IhfXHF8s-ZYk-rGmD1Cl2I0hf5Fe1R1_f9Uz5IeCnJ8/"
    "export?format=csv&gid=0"
)