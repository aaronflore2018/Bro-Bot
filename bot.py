import discord
import os
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
my_secret = os.environ['TOKEN']

@tasks.loop(seconds=15.0, count=2)
async def slow_count():
  print(slow_count.current_loop)

@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('+francothicc'):
      user = '<@355859329557069834>'
      await message.channel.send('This is a reminder to ' + user + ' that you are lookin extra thicc today')
    
    if message.content.startswith('+choose'):
        choices = message.content[7:].rsplit('|')
        chosen = random.choice(choices)
        quotes = ["Hmmmm well see, the thing is that **" + chosen + "** is just the right answer bro, hands down","Ay look, bro to bro, it's **" + chosen +"**", "Eh, I don't feel like it", "The Andres Scale says: **" + chosen + "**",]
        await message.channel.send(random.choice(quotes))

    if message.content.startswith('+commands'):
        await message.channel.send(file=discord.File('commands.txt'))


    if message.content.startswith('+downbad'):
        pics = [
          'https://cdn.discordapp.com/attachments/332364177140088834/835577831735689307/unknown.png',
          'https://cdn.discordapp.com/attachments/332364177140088834/835351625405169704/nfolf90vuzu61.png',
          'https://cdn.discordapp.com/attachments/332364177140088834/834586660334993408/st3gwwy75ku61.png',
          'https://cdn.discordapp.com/attachments/332364177140088834/833558730343841792/ErNW2Xd.png'
        ]
        chosen = random.choice(pics)
        await message.channel.send(chosen)
    
    if message.content.startswith('+quote'):
        quoteparts = message.content[7:].rsplit('"')
        name = quoteparts[0].strip()
        quote = quoteparts[1].strip()
        if "quotes" in db.keys():
          if str(name) in db["quotes"]:
            quotes = db["quotes"][name]
            quotes.append(quote)
            db["quotes"][name] = quotes
            await message.channel.send("Quote Added to " + name)
          else:
            db["quotes"][name] = [quote]
            await message.channel.send("Quote Added to " + name)
        else:
          db["quotes"] = {name: [quote]}
          await message.channel.send("Quote Added to " + name)


    if message.content.startswith('+qlist'):
      name = message.content[7:].strip()
      if "quotes" in db.keys():
        if name in db["quotes"]:
          quotes = db["quotes"][name]
          msg = "Here are all the quotes from " + name + ": \n"
          index = 0 
          for x in quotes:
            index += 1
            msg = msg + str(index) + ". " + x + "\n"
          await message.channel.send(msg)
        else:
          await message.channel.send("Couldn't find name in DB")
      else:
        await message.channel.send("Couldn't find the quote DB")

    if message.content.startswith('+cleardb'):
      db.popitem()
      await message.channel.send("Database Cleared")

    if message.content.startswith('+randq'):
      name = message.content[7:].strip()
      if "quotes" in db.keys():
        if name in db["quotes"]:
          quotes = db["quotes"][name]
          chosen = "\"" + random.choice(quotes) + "\" -" + name
          await message.channel.send(chosen)
        else:
          await message.channel.send("Couldn't find name in DB")
      else:
        await message.channel.send("Couldn't find the quote DB")

    if message.content.startswith('+name'):
      name = message.content[6:].strip()
      guilds = client.guilds
      print(guilds)
      guild = client.get_guild(message.guild.id)
      print(guild)
      member = guild.get_member_named(name)
      print(member)
      await message.channel.send(str(member.id))

    if message.content.startswith('+mememute'):
      name = message.content[12:-1].strip('!')
      print(name)
      guilds = client.guilds
      guild = client.get_guild(message.guild.id)
      member = guild.get_member(int(name))
      if(member == None):
        await message.channel.send("Cant find person in server")
      else:
        if member.voice != None and member.voice.mute == False:
          @slow_count.before_loop
          async def before_slow_count():
            print("Starting timer")
            await member.edit(mute=True)
            await message.channel.send("**" + member.name + "** muted for 15 seconds.")

          @slow_count.after_loop
          async def after_slow_count():
            print("Ending timer")
            await member.edit(mute=False)
        elif member.voice == None:
          await message.channel.send("Cant find person in voice channel")
        slow_count.start()
    
    if message.content.startswith('+unmute'):
      name = message.content[10:-1].strip()
      print(name)
      guilds = client.guilds
      guild = client.get_guild(message.guild.id)
      member = guild.get_member(int(name))
      if(member == None):
        await message.channel.send("Cant find person in server")
      else:
        if member.voice != None and member.voice.mute == True:
          await member.edit(mute=False)
  
keep_alive()
client.run(os.getenv('TOKEN'))