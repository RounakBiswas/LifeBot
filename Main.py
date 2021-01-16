import discord
from discord.ext import commands
import os
import json
import requests
import random
from replit import db
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary

client = discord.Client()
bot = commands.Bot(command_prefix = "$", case_sensitive=True)

sadWords = ["sad", "depressed", "angry", "miserable", "bad"]

happyWords = ["happy", "good", "fine", "cool", "excited"]

good_mood_words = ["Good Going", "Great", "Well Done", "Hope your day goes good", "That's my man", "Good Job"]

starter_encouragements = [
    "Cheer Up!", "Hang In There", "You're Great", "You are the best!"
]

day_predictions = ["You're day will go good", "It's going to be great", "Maybe you'll find something lucky", "I doubt it'll go bad", "No comments...", "Oh its gonna be horrible", "Full of surprises", "You may want to look out", "Bro , just chill it's gonna go gooood", "What do you think i am a bot ?", "Who knows , maybe you'll get a promotion", "You'll get betrayed", "Something terrible maybe?"]

suggestions = []

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "-" + json_data[0]['a']
    return (quote)

def get_joke():
  os.system("pip install requests -q")
  g = requests.get("https://official-joke-api.appspot.com/jokes/random")

  jokes = g.json()
  return(f"{jokes['setup']} \n {jokes['punchline']}")


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

def update_suggestions(suggestions_users):
    if "Usersuggestions" in db.keys():
        Usersuggestions = db["Usersuggestions"]
        Usersuggestions.append(suggestions_users)
        db["Usersuggestions"] = Usersuggestions
    else:
        db["Usersuggestions"] = [suggestions_users]


def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

def SearchWord(word):
  try:
    myDict = PyDictionary(word)
    return(myDict.getMeanings())
  except:
    return("Not Found")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sadWords):
      await message.channel.send(random.choice(options))

    if any(word in msg for word in happyWords):
      await message.channel.send(random.choice(good_mood_words))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New Encouragement added")

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$commands"):
      await message.channel.send('''1.$hello - Replies Hello
      2.$inspire - Gives you a inspirational quote
      3.$new - Adds new cheering word you type after $new
      4.$list- Lets you see the cheering words given by users
      5.If you type the words sad , depressed , miserable , angry , bad you will get a cheering word
      6.$commands - lets you see all the commands
      7.$predictmyday - gives a prediction for your day
      8.$suggest - this is a new bot so i am looking for suggstions to update, it works same as new command
      9.$joke - gets you a random joke
      10.$meaning - tells you the meaning of the specific word
      ''')
      
    if msg.startswith("$predictmyday"):
      await message.channel.send(random.choice(day_predictions))

    if msg.startswith("$suggest"):
      suggestions_users = msg.split("$suggest", 1)[1]
      update_suggestions(suggestions_users)
      await message.channel.send("Suggestion Added , Thank you for suggesting")

    if msg.startswith("$seeSuggestions"):
      Usersuggestions = []
      if "Usersuggestions" in db.keys():
        Usersuggestions = db["Usersuggestions"]
      await message.channel.send(Usersuggestions)

    if msg.startswith("$joke"):
      joke = get_joke()
      await message.channel.send(joke)

    if msg.startswith("$meaning"):
      meaningWord = msg.split("$meaning", 1)[1]
      meaning = SearchWord(meaningWord)
      await message.channel.send(meaning)

keep_alive()
client.run(os.getenv('TOKEN'))
