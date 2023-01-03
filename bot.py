import config
import discord
import sqlite3
from discord.ext import commands
from PokemonRequestHandler import PokemonRequestHandler

bot = commands.Bot(command_prefix="p!", intents = discord.Intents.all())
handler = PokemonRequestHandler()

@bot.event
async def on_ready():
    print("Bot is online")

@bot.command()
async def drop(e):
    await handler.spawn(e)

@bot.event
async def on_reaction_add(reaction, user):
    await handler.claim(reaction, user, bot)

@bot.command()
async def collection(e):
    await handler.showCollection(e)

@bot.command()
async def view(e, *, index):
    await handler.showOne(e, index)

@bot.command()
async def release(e, *, index):
    await handler.deleteOne(e, index)

bot.run(config.token)