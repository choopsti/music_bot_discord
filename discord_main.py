import discord
import youtube_dl
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix = "!")

@bot.command()
async def play(ctx, msg):
    channel = ctx.author.voice.channel #msg
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send("connected to the voice channel, " + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    a = 'https://www.google.com/search?q='+msg+'&oq='+msg+'&aqs=chrome..69i57j0i433i512j0i512l8.900j0j15&sourceid=chrome&ie=UTF-8'
    data = requests.get(a,headers=headers)
    bs4 = BeautifulSoup(data.text, 'html.parser')
    test = bs4.find("h3", {"class": "H1u2de"})
    test = test.select("a")
    test = test[0]['href']
    URL = test
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()


bot.run("ODg5MTA3MzAxOTY4MDE5NTA4.YUcbsw.SZKG8OX6eNpuVw6p_sdlmsvtjf4")
