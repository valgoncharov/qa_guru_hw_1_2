import os

import dotenv
import pytest


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url() -> str:
    return os.getenv("APP_URL")
