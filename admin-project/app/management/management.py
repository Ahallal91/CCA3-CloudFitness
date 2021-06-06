import requests
import os
class Management:
    api = "https://api.cloudfitness.click/exercises"
    key = os.environ["API_GATEWAY_KEY"]
    
    def get_exercise_by_approval(self, approval):

        if approval == True:
            response = requests.get(f'{self.api}/approved')
        else:
            response = requests.get(f'{self.api}/pending')
        return response.json()
        
    
    def update_exercise_approval(self, type, name, approval):
        headers = {'x-api-key': self.key }
        response = requests.put(f'{self.api}', 
                                headers=headers,
                                params={
                                    'approval' : approval,
                                    'exercisetype': type,
                                    'exercisename': name
                                }
        )
        return response.json()
