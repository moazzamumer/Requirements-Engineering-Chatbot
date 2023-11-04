import openai
import datetime
from models import *
from crud import *



class API():
   
   def __init__(self,  prompt = None , ):
        
        API_KEY = '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'
        openai.api_key = API_KEY  
        self.prompt = prompt

   def Basic_chat(self  ):
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            max_tokens = 200,
            temperature = 0.8,
            messages = [
               { "role" : "system" , "content" : "You are a requirements gathering assistant. Your goal is to collect detailed project requirements from the client by specific questioning. Please ask the client for information like modules of project, description, specific technologies for each module \
                 and any other relevant details and preferences when client starts to explain its project. Be thorough and ask for clarification if needed." },
                {"role": "user", "content": f" {self.prompt}" },
            ])
        message = response.choices[0]['message']
        return str(message['content'])
        
