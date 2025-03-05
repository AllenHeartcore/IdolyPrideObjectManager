from ..log import Logger

import yaml


logger = Logger()


def read_api_key():
    with open("../../../credentials.yml", "r") as file:
        credentials = yaml.safe_load(file)
        key = credentials.get("openai_api_key")
        if not key.startswith("sk-"):
            raise ValueError
        return key


class GPTImageCaptionEngine:

    def __init__(self):
        try:
            import openai

            openai.api_key = read_api_key()
            self.client = openai.Client()
            self.active = True
            logger.success("GPTImageCaptionEngine active")

        except:
            self.active = False

    def generate_caption(self, image_path):

        if not self.active:
            logger.warning("GPTImageCaptionEngine inactive")
            return ""
