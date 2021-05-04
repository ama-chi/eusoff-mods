import json
def initialise_account(user):
    with open('data.json', 'r+') as f:
        data = json.load(f)
        username = str(user)
        if username not in data['accounts']:
            data['accounts'][username] = {}



        
initialise_account('hi')