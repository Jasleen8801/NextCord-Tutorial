import os
from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord
import requests
import json
import random
from PIL import Image, ImageFont, ImageDraw
import textwrap

from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ui import Button, View

links = json.load(open("gifs.json"))

# load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name='hi')
async def SendMessage(ctx):
    await ctx.send('Hello!')

@bot.command(name="pic")
async def pic(ctx):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_link = response.json()['message']
    await ctx.send(image_link)

@bot.command(name="gif", aliases=["feed", "play", "sleep"])
async def gif(ctx):
    await ctx.send(random.choice(links[ctx.invoked_with]))

@bot.command(name='speak')
async def speak(ctx, *args):
    msg = " ".join(args)
    font = ImageFont.truetype("PatrickHand-Regular.ttf", 50)
    img = Image.open('dog.jpg')
    cx, cy = (350, 230)

    lines = textwrap.wrap(msg, width=20)
    w, h = font.getsize(msg)
    y_offset = (len(lines) * h)/2
    y_text = cy - (h/2) - y_offset

    for line in lines:
        draw = ImageDraw.Draw(img)
        w, h = font.getsize(line)
        draw.text((cx-(w/2), y_text), line, (0,0,0), font=font)
        img.save("dog-edited.jpg")
        y_text += h
    with open("dog-edited.jpg", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)

@bot.command(name="support")
async def support(ctx):
    hi = Button(label="Click Me", style=ButtonStyle.blurple)
    tutorial = Button(label="Tutorial", url="https://www.youtube.com/@Dannycademy")

    async def hi_callback(interaction):
        await interaction.response.send_message("Hello Coder!!!")
    
    hi.callback = hi_callback   

    myview = View(timeout=180)
    myview.add_item(hi)
    myview.add_item(tutorial)

    await ctx.send("hi", view=myview)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = Embed(title="Slow it down bro!", description=f"Try again in {error.retry_after:.2f}s", color=Color.red())
        await ctx.send(embed=em)

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
