from discord.ext import commands
from dotenv import load_dotenv
import keep_alive
import os

load_dotenv() #command_prefix.lower() = 'plz'??
bot = commands.Bot(command_prefix = ['plz ', 'Plz ', 'PLZ ', 'pLz', 'pLZ', 'plZ', 'PlZ', 'plZ', 'PLz']) 
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive.keep_alive()
bot.run(os.getenv("TOKEN"))