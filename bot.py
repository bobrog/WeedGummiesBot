#!/usr/bin/env python3

import discord
import random
import configargparse

client = discord.Client()

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
    # setup/process args
    parser = configargparse.ArgParser()
    parser.add("-t", "--bot-token", env_var="BOT_TOKEN", required=True, help="Discord bot API token")
    parser.add("-f", "--theme-file", env_var="THEME_FILE", default="themes.txt", help="File comtaining themes one per line")
    opts = parser.parse_args()
    #parser.print_values()
    
    # get the themes
    with open(opts.theme_file, "r") as f:
        list_of_themes = f.read().splitlines()
   
    # do it live!
    client.run(opts.bot_token)
