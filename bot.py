import discord
import random

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('WEED!')

    if message.content.startswith('$newtheme'):
        theme = random.choice(list_of_themes)
        await message.channel.send(theme)

if __name__ == "__main__":

    list_of_themes = ["country adjacent","hand claps","Doyle's imaginary jukebox","Brunch","Hype trax","Sad highschool","Jersey turnpike","Mass turnpike","vanlife","Pacific coast highway","whaling shanties","whaling protest songs","sleigh bells","ass claps","vocalists most would agree do not have a traditionally good singing voice","better the second time","brain fuzz","Warm up music for the NBA all star game ","Theme songs ","Poop","Fishing songs ","Songs where more than one person sings a verse (or part of a verse). ","Sounds like the future ","The kids are alright","Songs with whistling","Animal songs ","Songs my mom would like","Weed Gummy","Monster songs","fever and chills","Connecticut Pizza","Harsh Limits","plumbing","interstate 10","my favorite country songs","my jam in high school","Should have been added to the THPS remake ","b side","dancing the night away","Drunkest I've ever been","straight edge","horn-y","under the covers","I'm freaking out, maaaan","courting mode","shower sex","Side Saddle","Songs with talking"]

    client = discord.Client()
    client.run('token')
