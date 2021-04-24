import discord
import os
import random

client = discord.Client()
my_secret = os.environ['TOKEN']

@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('+hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('+choose'):
        choices = message.content[7:].rsplit('|')
        chosen = random.choice(choices)
        await message.channel.send('Hmmmm well see, the thing is that **' + chosen + '** is just the right answer bro, hands down')
  

client.run(os.getenv('TOKEN'))