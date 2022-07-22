import openai
from openai.error import RateLimitError
import time
from typing import Any
import logging
logger = logging.getLogger("openai")
logger.disabled = True


class Completion:
    def __init__(
        self,
        engine: str,
        stop: list[str],
        temperature: float,
        max_completion_tokens: int
    ) -> None:
        self.engine = engine
        self.stop = stop
        self.temperature = temperature
        self.max_completion_tokens = max_completion_tokens
        self.max_num_tries = 5

    def create(self, prompt: str) -> str:
        kwargs: dict[str, Any] = {
            "temperature": self.temperature, 
            "prompt": prompt,
            "max_tokens": self.max_completion_tokens,
            "stop": self.stop
        }
        kwargs["engine"] = self.engine
        num_tries: int = 0
        while num_tries < self.max_num_tries:
            try:
                response = openai.Completion.create(**kwargs)
                return response.choices[0].text
            except RateLimitError as error:
                #print(f"RateLimitError {num_tries+1}/{self.max_num_tries}")
                num_tries += 1
                time.sleep(30)
        raise Exception(f"Failed to create completion after {num_tries} tries")
