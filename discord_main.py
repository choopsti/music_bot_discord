import discord
from youtube_dl import YoutubeDL
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from discord import FFmpegPCMAudio


bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('disocrd.py'))

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="명령어 종류", color=0x62c1cc)
    embed.add_field(name="!명령어", value="명령어 종류가 나온다", inline=False)
    embed.add_field(name="!나가", value="음성채널 퇴장", inline=False)
    embed.add_field(name="!재생", value="음성채널 참가및 노래재생", inline=False)

@bot.command()
async def 재생(ctx, msg):
    global vc 
    vc = await ctx.message.author.voice.channel.connect()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    a = 'https://www.google.com/search?q='+msg+'&oq='+msg+'&aqs=chrome..69i57j0i433i512j0i512l8.900j0j15&sourceid=chrome&ie=UTF-8'
    data = requests.get(a,headers=headers)
    bs4 = BeautifulSoup(data.text, 'html.parser')
    test = bs4.find("h3", {"class": "H1u2de"})
    test = test.select("a")
    test = test[0]['href']
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(test, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + test + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")
    



@bot.command()
async def 나가(ctx):
    await bot.voice_clients[0].disconnect()


bot.run("ODg5MTA3MzAxOTY4MDE5NTA4.YUcbsw.SZKG8OX6eNpuVw6p_sdlmsvtjf4")
