"""Where the tests find BooKing Lab. Every value comes from an environment variable.

    API_URL   the API, default http://localhost:8000 (the local copy from docker-compose.yml)
    WEB_URL   the website, default http://localhost:5173
    COHORT    your cohort code, default DEMO (the open cohort for self-study)
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_url: str
    web_url: str
    cohort: str


def load_settings() -> Settings:
    return Settings(
        api_url=os.environ.get("API_URL", "http://localhost:8000").rstrip("/"),
        web_url=os.environ.get("WEB_URL", "http://localhost:5173").rstrip("/"),
        cohort=os.environ.get("COHORT", "DEMO"),
    )
