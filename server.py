from inspect import findsource
import discord
from discord import state
import requests

TRN_API_KEY = "a32626f3-c4ef-4e8a-807d-68e75bb27002"
DISCORD_BOT_TOKEN = "ODE0MDk5ODg2MzQ5MzUyOTcw.YDY7mg.AQZ6yZnLpKqUEgMkkk7RY_QP9YI"
HEADERS_TRN = {"TRN-Api-Key": TRN_API_KEY}

def find_stats(platform, username):
    if platform == "ps4":
        platform = 'psn'
    final_str = ""
    url = f"https://api.fortnitetracker.com/v1/profile/{platform}/{username}"
    response = requests.get(url, headers=HEADERS_TRN)
    try:
        data = response.json()["lifeTimeStats"][7:]
        for dict in data:
            row = ""
            i=0
            for key,value in dict.items():
                if i == 0:
                    row += f"**{value}** : "
                else:
                    row += f"{value}"
                i+=1
            final_str += f"{row}\n"
    except KeyError:
        final_str = f"Sorry but we don't found {username} with {platform} stats. Please try again."
    finally:
        return final_str

def find_shop():
    url="https://api.fortnitetracker.com/v1/store"
    response = requests.get(url, headers=HEADERS_TRN)
    return response.json()

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("$stats platform name"))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$stats'):
        msg_to_list = message.content.split(' ')
        pseudo = " ".join(msg_to_list[2:])
        stats = find_stats(msg_to_list[1], pseudo)
        await message.channel.send(stats)

    if message.content.startswith('$shop'):
        await message.channel.send("t'as pas assez d'argent tkt")

client.run(DISCORD_BOT_TOKEN)