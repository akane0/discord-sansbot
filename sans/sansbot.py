import discord
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix=".")
token = ""
players = {}
client.mystatus = "off"
client.already_running = False

@client.event
async def on_ready():
    print("-------")
    print("Logged in as:")
    print("User: " + client.user.name + "#" + client.user.discriminator)
    print("ID: " + client.user.id)
    print("SansBot")
    print("-------")


@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author == client.user or message.author.bot:
        return

    if client.mystatus != "on":
        return

    if client.already_running is True:
        return

    server = message.server
    sentence = message.content
    author = message.author
    channel = author.voice.voice_channel
    client.already_running = True

    word_list = sentence.split()

    voice = client.voice_client_in(server)

    for word in word_list:

        character_list = list(word)
        characters = len(character_list)

        if characters >= 16:
            soundfile = "sans_long.mp3"
            delay = 3.0
        elif characters >= 7:
            soundfile = "sans_medium.mp3"
            delay = 2.0
        else:
            soundfile = "sans_small.mp3"
            delay = 1.5

        player = voice.create_ffmpeg_player(soundfile)
        players[server.id] = player

        player.start()

        await asyncio.sleep(delay)

    client.already_running = False


@client.command(pass_context=True)
async def sans(ctx, status=""):

    if status == "on":
        client.mystatus = "on"
        print("Status: on.")

        try:
            voice = await client.join_voice_channel(ctx.message.author.voice.voice_channel)
            await client.send_message(ctx.message.channel, "*uhh uhhhhh* (online)")
        except:
            await client.say("User is not in channel.")
            client.mystatus = "off"

    elif status == "off":
        await client.send_message(ctx.message.channel, "*uhh uhhhh* (offline)")
        client.mystatus = "off"
        print("Status: off.")

        voice_client = client.voice_client_in(ctx.message.server)

        await voice_client.disconnect()

    else:
        await client.send_message(ctx.message.channel, "*uhhh uhhh uhhhh uh uh uhhhh* (missing argument:** `on | off`)")

client.run(token)
