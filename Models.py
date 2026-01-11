import os
from groq import Groq
import logging
logger = logging.getLogger(__name__)
class Model:
    def __init__(self,model="",name="Model"):
        self.client = None
        self.model = model
        self.name = name
    def __getattribute__(self, name):
        atr = super().__getattribute__(name)
        if name not in ["__init__","__getattribute__","connect","request"] and callable(atr):
            def new_func(*args, **kwargs):
                print(self.name,":",name)
                return atr(*args, **kwargs)
            return new_func
        return atr
    def options(self):
        pass
    def request(self, message):
        pass
    def respond(self, message):
        self.connect()
        try :
            return self.request(message)
        except Exception as e:
            logger.error("Error during Groq API call: %s", e)
            raise e
    def connect(self,KEY_NAME = "GROQ_API_KEY"):
        try :
            if self.client is None:
                import dotenv
                dotenv.load_dotenv()
                self.client = Groq(api_key=os.environ.get(KEY_NAME))
                logger.info("Connected to Groq API successfully.")
        except Exception as e:
            logger.error("Error connecting to Groq API: %s", e)
            raise e

class LLMModel(Model):
    def __init__(self,model="Llama-3.1-8B-Instant",name = "LLM Model"):
        super().__init__(model,name)
        self.temp = 1
        self.max_tokens = 1024
    def options(self, temp=1, max_tokens=1024,model = "Llama-3.1-8B-Instant"):
        self.temp = temp
        self.max_tokens = max_tokens
        self.model = model
    def request(self, message):
        completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=self.temp,
                max_completion_tokens=self.max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )
        return completion.choices[0].message.content

class TextToSpeachModel(Model):
    def __init__(self,model="canopylabs/orpheus-v1-english",name="Text To Speach Model"):
        super().__init__(model,name)
        self.voice = "autumn"
        self.format = "wav"
    def options(self, voice="autumn", format="wav", model="canopylabs/orpheus-v1-english"):
        self.voice = voice
        self.format = format
        self.model = model
    def request(self,text):
        response = self.client.audio.speech.create(
        model=self.model,
        voice=self.voice,
        response_format=self.format,
        input=text,
        )
        return response