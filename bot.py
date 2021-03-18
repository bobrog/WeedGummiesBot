#!/usr/bin/env python3

import os
import random
import configargparse
import gspread
import logging
import json
import datetime
import pytz
import discord
from discord.ext import tasks, commands

bot = commands.Bot("+", help_command=None)

def get_music_channel():
    return discord.utils.get(
                bot.get_all_channels(),
                name=opts.reminder_chan_name,
                type__name=discord.ChannelType.text.name)

def gsheet_themes():
    worksheet = gsheet.worksheet(opts.gsheet_worksheet)
    themes = worksheet.col_values(opts.gsheet_col)[opts.gsheet_col_offset:]
    return list(filter(None, themes))

def get_stonerism():
    # stoner speak
    global stoner_offset
    if stoner_offset > len(stoner_sayings) - 1:
        stoner_offset = 0
    say = stoner_sayings[stoner_offset]
    stoner_offset = stoner_offset + 1
    logging.info("stoner: {}".format(say))
    return(say)

def get_theme(fmt="{}"):
    try:
        say = fmt.format(random.choice(list_of_themes()))
    except IndexError:
        say = "Theme list is empty!"

    return say

@bot.command()
async def help(ctx):
    logging.info("help msg")
    helpemb = discord.Embed(
            description="** WeedGummies is a kinda buggy, kinda high bot **"
                + "\n <@{}> for deep thoughts".format(bot.user.id)
                + "\n\n ** Music Stuff **"
                + "\n Selects a new playlist theme Sunday afternoon in \
                    <#{}>".format(getattr(get_music_channel(), "id",
                        opts.reminder_chan_name))
                + "\n `+newtheme` draw a random theme from the spreadshite",
                colour=0x67eb34,
            )
    await ctx.send(embed=helpemb)

@tasks.loop(seconds=3600)
async def newtheme_task():
    logging.info("newtheme_task: woke up")
    channel = get_music_channel()

    if channel == None:
        logging.warning("newtheme_task: '{}' id not found".format(
            opts.reminder_chan_name))
        return

    logging.info("newtheme_task: '{}' has id {}".format(
        opts.reminder_chan_name,
        channel.id))

    # get current time
    now = datetime.datetime.now(tz=pytz.timezone(opts.reminder_tz))
    day = now.strftime("%A")
    hour = now.hour
    minute = now.minute
    #check if in fire window
    if day == "Sunday" and hour == 13:
        say = random.choice(reminder_sayings)
        logging.info("newtheme_task: {}".format(say))
        await channel.send(say)
    elif day == "Sunday" and hour == 15:
        say = get_theme("The new playlist theme is ... {}")
        logging.info("newtheme_task: {}".format(say))
        await channel.send(say)
    else:
        logging.info("newtheme_task: nothing to do")

@bot.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(bot))
    newtheme_task.start()

@bot.command()
async def weed(ctx):
    await ctx.send(get_stonerism())

@bot.listen("on_message")
async def weed_listen(message):
    if message.author == bot.user:
        return

    if bot.user.id in [ m.id for m in message.mentions ]:
        await message.channel.send(get_stonerism())

@bot.command()
async def newtheme(ctx):
    say = get_theme("Here is a theme ... {}")
    logging.info("newtheme: {}".format(say))
    await ctx.send(say)

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
    parser.add("--reminder-tz", env_var="REMINDER_TZ",
                default="America/New_York")
    parser.add("--reminder-chan-name", env_var="REMINDER_CHAN_NAME",
                default="music-andotherstuffrelated")
    parser.add("--reminder-file", env_var="REMINDER_FILE",
                default="reminder.txt")

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

    stoner_offset = random.randint(0, len(stoner_sayings) - 1)

    # init reminder messages
    if opts.reminder_file != None and os.path.isfile(opts.reminder_file):
        with open(opts.reminder_file, "r") as f:
            reminder_sayings = f.read().splitlines()
        logging.info("reminders speak from file {}".format(opts.reminder_file))
    else:
        reminder_sayings = ["New playlist theme drops soon! " \
                            "Get your suggestions into the spreadshite"]

    # do it live!
    bot.run(opts.discord_token)
