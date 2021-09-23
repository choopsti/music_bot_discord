import discord
from youtube_dl import YoutubeDL
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from discord import FFmpegPCMAudio
import os
import asyncio
from discord.ext import commands
client = commands.Bot(command_prefix='!')
songs = asyncio.Queue()
play_next_song = asyncio.Event()
@client.event
async def on_ready():
    print('client ready')
async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()
def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)
@client.command(pass_context=True)
async def play(ctx, url):
    if not client.is_voice_connected(ctx.message.server):
        voice = await client.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = client.voice_client_in(ctx.message.server)
    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)
client.loop.create_task(audio_player_task())

access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
