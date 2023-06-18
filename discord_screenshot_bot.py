#!/usr/bin/env python3

#Script Purpose: A Gloveworks Discord Screenshot Bot to take screenshots on request or on intervals

#purpose: schedules the discord bot to take screenshots
from apscheduler.schedulers.background import BackgroundScheduler
#purpose: necessary for automating/interacting with a browser
from selenium import webdriver
#purpose: necessary for making sure the browser can be interacted with in a docker environment
from selenium.webdriver.chrome.options import Options
#purpose: imports utc timezone so that daylight saving time does not affect the scheduler
from pytz import utc

import asyncio #purpose: async/coroutine support 
import datetime #purpose: to timestamp inputs
import discord #purpose: allows for discord api calls
import os #purpose: allows to remove the screenshot file, grab the discord token as environment variable
import re #purpose: supports sanitizing input to make sure the URL is properly formatted
import uuid #purpose: unique screenshot names to avoid deleting the wrong screenshot requests

### -- GLOBAL VARIABLES ###
#Grab the token that was passed to the docker container
token = os.environ['DISCORD_TOKEN']
#official channel id of gloveworks' update channel
channel_id = 692925474032320542
#alert everyone the monthly contest is over
global_here = "here"
#default input message to take a screenshot of gloveworks website
default_input_msg = "!screenshot https://stats.mygloveworks.com/players/csgo"

#initialize the discord bot
client = discord.Client(intents=discord.Intents.default())

#callback function that is called when the bot is initialized
#here is where we schedule the bot to take screenshots on interval
@client.event
async def on_ready():
    #announce the bot activated
    print(f"[{datetime.datetime.now()}] Successfully Booted Up Discord Bot")
    #initialize the scheduler
    sched = BackgroundScheduler()
    #configure the scheduler to take a screenshot on the
    #by passing the function "scheduled_job"
    #This uses UTC time so 2 AM UTC is 7 PM PST
    #so the first day of the month in UTC is the last day in PST
    sched.add_job(scheduled_job, 'cron', day=1, hour=2, timezone=utc)
    #start the scheduler
    sched.start()

#function that will be called every time the scheduler wakes up
def scheduled_job():
    #Announce we're taking an automated screenshot
    print("[{0}] It's that time of the month again: time to take a screenshot!".format(datetime.datetime.now()))
    #use the default message so we take a screenshot of gloveworks' top player website
    message = default_input_msg
    #create the discord channel object based on the channel id
    channel = client.get_channel(channel_id)
    #since all of the discord async routines are coroutine - add it to the client's loop
    asyncio.run_coroutine_threadsafe(grab_screenshot(message, global_here, channel), client.loop)

#this is mostly used for testing if the bot works or not
#callback function that will be called when the discord bot receives a message
@client.event
async def on_message(message):
    #if the command is screenshot let's consider it as a valid input for now...
    if "!screenshot" in message.content:
        print(f"[{datetime.datetime.now()}] [Server: {message.guild.name}][#{message.channel}][{message.author}]:'{message.content}'")
        #pass the message content to scrub, the author who sent it, and the channel object from the message
        await grab_screenshot(message.content, message.author.id, message.channel)

#main logic that takes a screenshot of a website
#takes in the following arguments:
# message: a string representing the message that was sent to the bot
# author_id: a string or int representing the sender of the message
# channel: a Discord Channel object that allows us to send messages back to the channel
async def grab_screenshot(message, author_id, channel):
    #initialize the options we will need to start chromium and interact with it
    chrome_options = Options()
    #headless is necessary in a docker environment 
    chrome_options.add_argument("--headless") 
    #chromium will complain and refuse to run if this isn't passed
    chrome_options.add_argument('--no-sandbox')

    #Perform a regular expression to make sure the input is a proper URL
    urls = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

    #if urls wasnt assigned anything then the message did not have a proper URL
    if urls is None:
        #if the author_id is the "here" string do not use the < > format
        #otherwise use the < > format because the user won't be @'d correctly
        if author_id == global_here:
            #send the message and make sure it's sent with 'await' because we are a async function
            await channel.send(f"@{author_id} make sure to paste the entire link (Include https:// or http://)")
        else:
            #send the message and make sure it's sent with 'await' because we are a async function
            await channel.send(f"<@{author_id}> make sure to paste the entire link (Include https:// or http://)")
        #return because an invalid message was passed
        return

    #start Chromium
    driver=webdriver.Chrome(options=chrome_options)
    #pass the URL to grab the HTML page
    driver.get(urls.group())
    #set the resolution for the screenshot
    driver.set_window_size(1920, 1080)    
    #generate a unique file name so we don't conflict with a parallel screenshot
    fileName = uuid.uuid4().hex[:6].upper() + ".png"
    #if the author_id is "here" don't use < > format
    #otherwise use the < > format so the user get's properly @'d
    if author_id == global_here:
        #Format the message - announce the screenshot correlates with the top 10 players
        #because this script is configured to be in UTC time - we need to subtract by one day
        currentdate = datetime.datetime.now() - datetime.timedelta(days=1)
        #grab the string format of the month
        month = currentdate.strftime("%B")
        #grab the string format of the year
        year = currentdate.strftime("%Y")
        #announce the top 10 players of the month
        await channel.send(f"@{author_id} Top 10 Players {month} {year}")
    else:
        #respond to the author who requested the screenshot
        await channel.send(f"<@{author_id}> Heres Your ScreenShot Of: {urls.group()}")
    #grab the screenshot
    driver.get_screenshot_as_file(fileName)
    #send the screenshot to the discord channel
    await channel.send(file=discord.File(fileName))
    #clean up the screenshot file so the machine never runs out of space
    os.remove(fileName)
    #close the browser
    driver.quit()


#if this python script was called let's start the main logic
if __name__ == "__main__":
    #Announce we are starting up
    print(f"[{datetime.datetime.now()}] Booting Up Discord Bot")
    #call the discord bot to "run" or to start
    client.run(token.strip())
