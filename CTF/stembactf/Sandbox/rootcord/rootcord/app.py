import os
import uuid
import subprocess

from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

FLAG = os.getenv("FLAG")
prefix = "~/"
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")

token = os.getenv("DISCORD_BOT_TOKEN")

if not token:
    raise RuntimeError("Please specify the token in .env file!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith(f"{prefix}run"):
        await handleRunCode(message)
        return

    await bot.process_commands(message)


async def handleRunCode(message: discord.Message):
    code = message.content[len(f"{prefix}run") :].strip(" \n`")
    if not code:
        await message.channel.send("Bruh, mana kodenya?")
        return

    if code.startswith("py"):
        code = code[len("py") :].strip(" \n`")

    if not code.isascii() or  "import" in code or "e" in code or "t" in code or "\\" in code:
        await message.channel.send("Oooopss, yaa gimana yaa bang hehehe:v")
        return

    # embed flag
    code = f"flag='{FLAG}'\n{code}"

    filename = f"{uuid.uuid4()}.py"
    with open(filename, "w") as f:
        f.write(code)

    execute = subprocess.Popen(
        ["python", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    execute.wait()

    os.remove(filename)

    stdout = execute.stdout.read().decode("utf-8")
    stderr = execute.stderr.read().decode("utf-8")

    if stdout:
        embed = discord.Embed(title="Output", color=0x00FF00)
        embed.description = f"```py\n{stdout}\n```"
    elif stderr:
        embed = discord.Embed(title="Error", color=0xFF0000)
        embed.description = f"```py\n{stderr}\n```"
    else:
        embed = discord.Embed(title="Output", color=0x00FF00)
        embed.description = "```py\nNo output\n```"

    await message.channel.send(embed=embed)


@bot.command(name="help")
async def help(ctx: commands.Context):
    embed = discord.Embed(
        title="Help", description="How to run code with this bot?", color=0x00FF00
    )
    embed.add_field(
        name="Run code",
        value=f"""
        ~/run
        \```py
        
        <code here>
        
        ```""",
        inline=False,
    )

    embed.add_field(
        name="Example",
        value="""
        ~/run
        \```py

        print("Hello World")
        
        ```
        """,
        inline=False,
    )
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(token)
