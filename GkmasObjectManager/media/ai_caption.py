from ..log import Logger

import yaml


logger = Logger()


def read_api_key():
    with open("../../credentials.yml", "r") as file:
        credentials = yaml.safe_load(file)
        key = credentials.get("openai_api_key")
        if not key.startswith("sk-"):
            raise ValueError
        return key


class GPTCaptionEngine:

    def __init__(self):
        try:
            import openai

            openai.api_key = read_api_key()
            self.client = openai.Client()
            self.active = True
            logger.success("GPTCaptionEngine active")

        except:
            self.active = False

    def generate(
        self,
        embed_url,
        prompt,
        max_tokens=150,
        temperature=0.5,
    ):

        if not self.active:
            logger.warning("GPTCaptionEngine inactive")
            return "[GPT captioning engine is inactive.]"

        return self.client.Completion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are a helpful assistant that provides concise yet descriptive
                        captions for multimedia content like images and audio.
                        The media content will be provided as a base64-encoded string.
                        """,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "content": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": embed_url,
                        },
                    ],
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        ).choices[0]
