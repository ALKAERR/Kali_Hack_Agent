"""Execution configuration for agents."""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import ModelSettings, set_default_openai_client, set_default_openai_api, set_tracing_disabled

load_dotenv(".env")

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

MODEL_CONFIG = ModelSettings(
    toolChoice="required"
)

