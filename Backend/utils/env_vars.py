import os
from dotenv import load_dotenv
import pathlib

BASEDIR = pathlib.Path(__file__).resolve()
PARENTDIR = BASEDIR.parent.parent

# Load environment variables from the .env file
response = load_dotenv(PARENTDIR.joinpath('.env'))
if not response:
    raise Exception('Environment variable not loaded!')

def get_env_var(var_name):
    """
    get environment variable from load_dotenv (located in .env file)
    """
    return os.getenv(var_name)