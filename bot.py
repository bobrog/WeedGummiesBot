#!/usr/bin/env python3

import discord
import random
import configargparse
import gspread

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
        theme = random.choice(list_of_themes())
        await message.channel.send(theme)

def gsheet_themes():
    themes = gsheet.col_values(opts.gsheet_col)[opts.gsheet_col_offset:]
    return list(filter(None, themes))

if __name__ == "__main__":
    # setup/process args
    parser = configargparse.ArgParser()
    parser.add("--config-file", is_config_file=True, help='config file path')
    parser.add("--discord-token", env_var="DISCORD_TOKEN", required=True, help="Discord bot API token")
    parser.add("--theme-file", env_var="THEME_FILE", default="themes.txt", help="File containing themes one per line")
    parser.add("--gsheet-creds-file", env_var="GSHEET_CREDS_FILE", help="Google API Service account key JSON file")
    parser.add("--gsheet-key", env_var="GSHEET_KEY")
    parser.add("--gsheet-worksheet", env_var="GSHEET_WORKSHEET")
    parser.add("--gsheet-col", env_var="GSHEET_COL", type=int)
    parser.add("--gsheet-col-offset", env_var="GSHEET_COL_OFFSET", type=int)

    opts = parser.parse_args()
    parser.print_values()
    
    if opts.gsheet_creds_file != None:
        # get themes from Google Sheet column
        gauth = gspread.service_account(filename=opts.gsheet_creds_file)
        gsheet = gauth.open_by_key(opts.gsheet_key).worksheet(opts.gsheet_worksheet)
        list_of_themes = gsheet_themes
    else:
        # get the themes from file
        with open(opts.theme_file, "r") as f:
             file_themes = f.read().splitlines()
             list_of_themes = lambda: file_themes

    # do it live!
    client.run(opts.discord_token)
