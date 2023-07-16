#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytz import utc
import asyncio
import datetime
import discord
import os
import re
import uuid

# Utils functions
def get_token():
    tok = os.environ.get("DISCORD_TOKEN")
    if not tok:
        raise Exception("Discord Token not found")
    return tok

def get_channel_id():
    try:
        return int(os.environ.get("CHANNEL_ID", 692925474032320542))
    except ValueError:
        print("Invalid lobby id provided. Defaulting to hardcoded value...")
        return 692925474032320542

# Global Variables
token = get_token()
channel_id = get_channel_id()
global_here = "here"
default_input_msg = "!screenshot https://stats.mygloveworks.com/players/csgo"
client = discord.Client(intents=discord.Intents.default())

# Callback when the bot is initialized, schedule screenshot
@client.event
async def on_ready():
    print(f"[{datetime.datetime.now()}] Successfully Booted Up Discord Bot")
    sched = BackgroundScheduler()
    sched.add_job(scheduled_job, 'cron', day=1, hour=2, timezone=utc)
    sched.start()

def scheduled_job():
    print("[{0}] It's that time of the month again: time to take a screenshot!".format(datetime.datetime.now()))
    message = default_input_msg
    channel = client.get_channel(channel_id)
    asyncio.run_coroutine_threadsafe(grab_screenshot(message, global_here, channel), client.loop)

# Callback when the bot receives a message
@client.event
async def on_message(message):
    if "!screenshot" in message.content:
        print(f"[{datetime.datetime.now()}] [Server: {message.guild.name}][#{message.channel}][{message.author}]:'{message.content}'")
        await grab_screenshot(message.content, message.author.id, message.channel)

# Main logic to take a screenshot of a website
async def grab_screenshot(message, author_id, channel):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')

    urls = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

    if urls is None:
        mention_format = f"<@{author_id}>" if author_id != global_here else f"@{author_id}"
        await channel.send(f"{mention_format} make sure to paste the entire link (Include https:// or http://)")
        return

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(urls.group())
    driver.set_window_size(1920, 1080)
    file_name = uuid.uuid4().hex[:6].upper() + ".png"

    if author_id == global_here:
        current_date = datetime.datetime.now() - datetime.timedelta(days=1)
        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")
        await channel.send(f"@{author_id} Top 10 Players {month} {year}")
    else:
        await channel.send(f"<@{author_id}> Here's Your Screenshot Of: {urls.group()}")

    driver.get_screenshot_as_file(file_name)
    await channel.send(file=discord.File(file_name))
    os.remove(file_name)
    driver.quit()

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Booting Up Discord Bot...")
    client.run(token.strip())
