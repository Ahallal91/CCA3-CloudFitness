import requests
class Management:
    api = "https://api.cloudfitness.click/workouts"
    key = "y6Ae5eqeM54tRx9AV1cSk9lGPmRwoDN46SEzPyHY"

    def get_exercise_by_approval(self, approval):
        response = requests.get(f'{self.api}?approval={approval}')
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
        print(response.json())
        return response.json()
