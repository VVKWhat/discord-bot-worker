import nextcord
from dotenv import load_dotenv

load_dotenv()

def main():
    token = open('token').read().strip()
    intents = nextcord.Intents.default()
    client = nextcord.Client(intents=intents)
    client.run(token)
    print('Bot started')

if __name__ == '__main__':
    main()

