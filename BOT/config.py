import os
from dotenv import load_dotenv

def get_token():
    # Assuming the token.env file is in the BOT/TOKEN directory
    env_path = os.path.join(os.path.dirname(__file__), 'TOKEN', 'token.env')
    load_dotenv(env_path)
    
    # Retrieve the Discord Token
    return os.getenv('DISCORD_TOKEN')

def get_owners():
    # Load the owners.env file
    owners_env_path = os.path.join(os.path.dirname(__file__), 'OWNER', 'owners.env')
    load_dotenv(owners_env_path)

    # Retrieve the owner IDs from the environment variables
    owners = []
    index = 1
    while True:
        owner_id = os.getenv(f'OWNER_{index}')
        if owner_id is None:
            break
        owners.append(int(owner_id))
        index += 1

    return owners