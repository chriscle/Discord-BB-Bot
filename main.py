#import required dependencies
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

#importing time module
import time

#import bot token
from apikeys import *

intents = discord.Intents.default()
intents.members = True

queues = {}

def check_queue(ctx, id):
    if queue[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

#confirmation in the console for when the bot is online
@client.event
async def on_ready():
    print("BB is now online.")
    print("-----------------")


#test commands hello and bye
@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am BB")

@client.command()
async def bye(ctx):
    await ctx.send("Cya later aligator")


#event for when people join/leave the channel
@client.event
async def on_member_join(member):
    channel = client.get_channel(551612250922811413)
    await channel.send("Hello! Someone has joined the server")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(551612250922811413)
    await channel.send("Goodbye. Someone has left the server")


#commands for bot to join and leave voice channels
@client.command(pass_context = True)
async def join(ctx):
    #detects if user is in a channel. If true, joins that specific channel and plays a sound file
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('MyPurpose.mp3')
        player = voice.play(source)
    else:
        await ctx.send("Please be in a voice channel to run this command")

@client.command(pass_context = True)
async def leave(ctx):
    #if bot is in voice channel then leave, else send error msg
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


#WORK IN PROGRESS
#if bot is in voice channel, play woof mp3
@client.command(pass_context = True)
async def woof(ctx):
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio('woof.mp3')
        player = voice.play(source)



#function to pause any audio currently playing. Bot must be in voice chat to use
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There is no audio playing")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is no audio paused")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg)
    palyer = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
    
@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    
    else:
        queues[guild_id] = [source]

    await ctx.send("Added to queue")


client.run(BOTTOKEN)
