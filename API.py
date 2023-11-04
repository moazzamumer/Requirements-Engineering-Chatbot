import openai
import datetime
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
            messages = [
                { "role":"system", "content":"Initiate a thorough exploration into the user's project. Start by extracting key details about their epics and sprint goals. \
                 Transition into technical specifics, including their preferred coding languages, frameworks, system architecture, and any associated versions or libraries. \
                 Delve into the dynamics of their team, capturing its size and the roles within. Understand their conventions, especially around naming and testing. With every response, dive deeper, asking iterative questions to ensure no stone is left unturned.\
                 As the user provides data, categorize and store it within the predefined data structure. Once you've gathered all the necessary details, you have to get the following information step by step from the client:\n\nprojectDetails\n  - epics\n  - sprintGoals\ntechnicalDetails\n  - languages\n  - frameworks\n  - architecture\n  - libraries\n  - versions\nteamDynamics\n  - size\n  - roles\nconventionsProcedures\n  - namingConventions\n  - testingProcedures\nadditionalInfo\n\nRetrieve information one by one and don't rush into questioning" },
                chat_array,
            ])
        message = response.choices[0]['message']
        return str(message['content'])
        
