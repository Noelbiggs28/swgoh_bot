import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
import random

from db_calls.how_many import get_number
from db_calls.rare import rare_plan
from db_calls.update_units import update_units
from db_calls.jedi2 import jedi2_plan
from db_calls.sith2 import sith2_plan
from db_calls.planet_check2 import planet_check2
from db_calls.planets2 import planets_check2
from db_calls.where import where_at
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

planet_choices = [
    discord.app_commands.Choice(name="Mustafar", value="Mustafar"),
    discord.app_commands.Choice(name="Corellia", value="Corellia"),
    discord.app_commands.Choice(name="Coruscant", value="Coruscant"),
    discord.app_commands.Choice(name="Geonosis", value="Geonosis"),
    discord.app_commands.Choice(name="Felucia", value="Felucia"),
    discord.app_commands.Choice(name="Bracca", value="Bracca"),
    discord.app_commands.Choice(name="Dathomir", value="Dathomir"),
    discord.app_commands.Choice(name="Tatooine", value="Tatooine"),
    discord.app_commands.Choice(name="Kashyyyk", value="Kashyyyk"),
    discord.app_commands.Choice(name="Zeffo", value="Zeffo"),
    discord.app_commands.Choice(name="Haven-class Medical Station", value="Haven-class Medical Station"),
    discord.app_commands.Choice(name="Kessel", value="Kessel"),
    discord.app_commands.Choice(name="Lothal", value="Lothal"),
    discord.app_commands.Choice(name="Malachor", value="Malachor"),
    discord.app_commands.Choice(name="Vandor", value="Vandor"),
    discord.app_commands.Choice(name="Ring of Kafrene", value="Ring of Kafrene"),
    discord.app_commands.Choice(name="Death Star", value="Death Star"),
    discord.app_commands.Choice(name="Hoth", value="Hoth"),
    discord.app_commands.Choice(name="Scarif", value="Scarif")
]

async def send_message(ctx, message):
    print("ping")
    if str(ctx.channel) in ["bot_test", "swgoh-bot-channel"]:
        if len(message) <= 2000:
            await ctx.send(message)
        else:
            chunks = [message[i:i + 2000] for i in range(0, len(message), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)

@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync()
    guild_id = os.getenv('GUILD_ID')  # Replace with your guild ID
    guild = discord.Object(id=guild_id)
    await bot.tree.sync(guild=guild)
    await send_message(ctx, "done")

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"hello {interaction.user.mention}", ephemeral=True)

@bot.hybrid_command(name="list", description="List various items")
@app_commands.describe(what_list="Choose a list to display")
@app_commands.choices(what_list=[
    app_commands.Choice(name="planets", value="planets"),
])
async def list(ctx: commands.Context, what_list: app_commands.Choice[str]):
    if what_list.value == "planets":
        x = 'Mustafar, Corellia, Coruscant, Geonosis, Felucia, Bracca, Dathomir, Tatooine, Kashyyyk, Zeffo, Haven-class Medical Station, Kessel, Lothal, Malachor, Vandor, Ring of Kafrene, Death Star, Hoth, Scarif'
    else:
        x = f"Unknown list: {what_list}"
    await send_message(ctx, x)

@bot.hybrid_command(name="how_many", description="Get the number of units and relic we have")
async def how_many(ctx: commands.Context, unit_name: str):
    try:
        x = get_number(unit_name)
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in how_many: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="where", description="Get what ops a unit is needed for")
async def where(ctx: commands.Context, unit_name: str):
    try:
        x = where_at(unit_name)
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in where: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="planet", description="Get units needed for a planet")
@app_commands.describe(planet_name="Choose a planet")
@app_commands.choices(planet_name=[
    app_commands.Choice(name="Mustafar", value="Mustafar"),
    app_commands.Choice(name="Corellia", value="Corellia"),
    app_commands.Choice(name="Coruscant", value="Coruscant"),
    app_commands.Choice(name="Geonosis", value="Geonosis"),
    app_commands.Choice(name="Felucia", value="Felucia"),
    app_commands.Choice(name="Bracca", value="Bracca"),
    app_commands.Choice(name="Dathomir", value="Dathomir"),
    app_commands.Choice(name="Tatooine", value="Tatooine"),
    app_commands.Choice(name="Kashyyyk", value="Kashyyyk"),
    app_commands.Choice(name="Zeffo", value="Zeffo"),
    app_commands.Choice(name="Haven-class Medical Station", value="Haven-class Medical Station"),
    app_commands.Choice(name="Kessel", value="Kessel"),
    app_commands.Choice(name="Lothal", value="Lothal"),
    app_commands.Choice(name="Malachor", value="Malachor"),
    app_commands.Choice(name="Vandor", value="Vandor"),
    app_commands.Choice(name="Ring of Kafrene", value="Ring of Kafrene"),
    app_commands.Choice(name="Death Star", value="Death Star"),
    app_commands.Choice(name="Hoth", value="Hoth"),
    app_commands.Choice(name="Scarif", value="Scarif")
])
async def planet(ctx: commands.Context, planet_name: app_commands.Choice[str], all: bool = True):
    try:
        x = planet_check2(planet_name.value, all)
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in where: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="planets", description="Get units for 2 planets combined")
async def planets(ctx: commands.Context, planet1: str, planet2: str, all: bool = True):
    try:
        x = planets_check2(planet1, planet2, all)
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in planets: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="sith_plan", description="Get what units were missing making ops impossible.")
async def sith_plan(ctx: commands.Context):
    try:
        x = sith2_plan()
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in sith_plan: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="jedi", description="Get units were short to complete in one go")
async def jedi(ctx: commands.Context):
    try:
        x = jedi2_plan()
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in jedi: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.hybrid_command(name="rare_plan", description="Get units we have exactly enough of")
async def rare_plan(ctx: commands.Context):
    try:
        x = rare_plan()
        await send_message(ctx, x)
    except Exception as e:
        logging.error(f"Error in rare_plan: {e}")
        await send_message(ctx, "An error occurred while processing your request.")

@bot.command()
async def update(ctx):
    await send_message(ctx, "This takes like 30 seconds")
    update_units()
    await send_message(ctx, "Guild updated")



@bot.command()
async def Ezls(ctx, crate):
    if crate.lower() == "crate":
        phrases = ["Knock, knock!","SteveO, is that you?!","Ax Brad, he’ll know what to do.",
                   "DILLY, DILLY!!","Is that babe @vpukam8621 still hanging around….oh, hey!",
                   "Yes, I’m!","Wanna here a guud joke?!", "https://tenor.com/3qw8.gif", 
                   "https://tenor.com/RJkK.gif",
                   "https://tenor.com/view/who-is-you-talking-looking-who-are-you-talking-about-look-up-gif-15744968"]
        
        x = random.choice(phrases)
        await send_message(ctx, x)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)


