from ..log import Logger

import yaml


logger = Logger()


def read_api_key():
    with open("credentials.yml", "r") as file:
        credentials = yaml.safe_load(file)
        key = credentials.get("openai_api_key")
        if not key.startswith("sk-"):
            raise ValueError
        return key


class GPTCaptionEngine:
    """Adapted from https://platform.openai.com/docs/guides/vision"""

    def __init__(self):
        try:
            import openai

            self.client = openai.Client(api_key=read_api_key())
            self.active = True

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
            return "[GPT captioning engine is inactive.]"

        return (
            self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a helpful assistant that provides concise yet descriptive
                        captions for images, typically anime-style illustrations.
                        The media content will be provided as a base64-encoded string.
                        """,
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": embed_url},
                            },
                        ],
                    },
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            .choices[0]
            .message.content
        )
