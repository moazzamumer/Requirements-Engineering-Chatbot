import openai
import datetime
import systemPrompts
from models import *
from crud import *

class API():
   
   def __init__(self,  prompt = None ):
        
        API_KEY = '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'
        openai.api_key = API_KEY  
        self.prompt = prompt

   def contextChat(self, chat_array):
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            max_tokens = 500,
            temperature = 0.8,
            messages = chat_array)
        message = response.choices[0]['message']
        return str(message['content'])
        
   def basicJSONMaker(self, client_chat):
          response = openai.ChatCompletion.create(
               model = 'gpt-3.5-turbo',
               max_tokens = 500,
               temperature = 0.8,
               messages = [{"role" : "system", "content" : systemPrompts.getBasicJSONMakerSystemPrompt()},
                         {"role" : "user", "content" : f"{client_chat}"}]
               )
          message = response.choices[0]['message']
          return str(message['content'])
       
