#!/usr/bin/env python3

import os
import random
import discord
import configargparse
import gspread
import logging
import json

client = discord.Client()

@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (message.content.startswith('$hello') or
        client.user.id in [ m.id for m in message.mentions ]):
        # stoner speak
        say = random.choice(stoner_sayings)
        logging.info("stoner: {}".format(say))
        await message.channel.send(say)
    elif message.content.startswith('$newtheme'):
        # theme
        say = random.choice(list_of_themes())
        logging.info("theme: {}".format(say))
        await message.channel.send(say)

def gsheet_themes():
    worksheet = gsheet.worksheet(opts.gsheet_worksheet)
    themes = worksheet.col_values(opts.gsheet_col)[opts.gsheet_col_offset:]
    return list(filter(None, themes))

if __name__ == "__main__":
    # setup/process args
    parser = configargparse.ArgParser()
    parser.add("--config-file", is_config_file=True, help='config file path')
    parser.add("--discord-token", env_var="DISCORD_TOKEN", required=True,
                help="Discord bot API token")
    parser.add("--theme-file", env_var="THEME_FILE", default="themes.txt",
                help="File containing themes one per line")
    parser.add("--stoner-file", env_var="STONER_FILE", default="stonertalk.txt",
                help="File containing stoner sayings")
    parser.add("--gsheet-creds", env_var="GSHEET_CREDS",
                help="Google API Service account key JSON string")
    parser.add("--gsheet-key", env_var="GSHEET_KEY")
    parser.add("--gsheet-worksheet", env_var="GSHEET_WORKSHEET")
    parser.add("--gsheet-col", env_var="GSHEET_COL", type=int)
    parser.add("--gsheet-col-offset", env_var="GSHEET_COL_OFFSET", type=int)
    parser.add("--log-level", env_var="LOG_LEVEL", default="INFO")

    opts = parser.parse_args()
    parser.print_values()

    # init logs
    logger_level = getattr(logging, opts.log_level.upper())
    logger_format = "%(asctime)s %(name)-20s %(levelname)-8s %(message)s"
    logging.basicConfig(level=logger_level,
                        format=logger_format)


    # init themes
    if opts.gsheet_creds != None:
        # get themes from Google Sheet column
        gauth_key = json.loads(opts.gsheet_creds)
        gauth = gspread.service_account_from_dict(gauth_key)
        gsheet = gauth.open_by_key(opts.gsheet_key)
        list_of_themes = gsheet_themes
        logging.info("themes from GSheets")
    else:
        # get the themes from file
        with open(opts.theme_file, "r") as f:
             file_themes = f.read().splitlines()
             list_of_themes = lambda: file_themes
        logging.info("themes from file {}".format(opts.theme_file))

    # init stoner speak
    if opts.stoner_file != None and os.path.isfile(opts.stoner_file):
        with open(opts.stoner_file, "r") as f:
            stoner_sayings = f.read().splitlines()
        logging.info("stoner speak from file {}".format(opts.stoner_file))
    else:
        stoner_sayings = ["i ran out of things to say"]

    # do it live!
    client.run(opts.discord_token)
