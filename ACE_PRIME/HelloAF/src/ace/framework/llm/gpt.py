# llm/gpt.py
import time
from typing import List, TypedDict, Optional

from openai import OpenAI

from ace.logger import Logger


class GptMessage(TypedDict):
    role: str
    name: Optional[str]
    content: str


class GPT:
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.client = OpenAI(
            max_retries=5,
            timeout=5.0,
        )

    def create_conversation_completion(
        self, model, conversation: List[GptMessage]
    ) -> GptMessage:
        self.log.info(f"conversation: {conversation}")

        count = 0
        while True:
            try:
                self.log.info("Creating conversation completion")
                start_time = time.time()
                
                chat_completion = self.client.chat.completions.create(
                    model=model, 
                    response_format={"type": "json_object"},
                    messages=conversation,
                    temperature=0.1,
                )
                break
            except Exception as e:
                end_time = time.time()
                self.log.error("Conversation completion took " + str(end_time - start_time))
                self.log.error("Error creating conversation completion: " + str(e))
                count += 1
                if count >= 5:
                    raise e
            
        end_time = time.time()
        self.log.info("Conversation completion took " + str(end_time - start_time))
        self.log.info("Chat completion: " + str(chat_completion))
        response = chat_completion.choices[0].message
        return response
        

    def create_image(self, prompt, quality="standard",  size="256x256") -> str:
        self.log.debug("Generating image for prompt: " + prompt)
        result = self.client.images.generate(
            size=size,
            prompt=prompt,
            quality=quality
        )
        image_url = result.data[0].url
        self.log.debug(
            ".... finished generating image for prompt" + prompt + ":\n" + image_url
        )
        return image_url
