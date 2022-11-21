import os
# from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord
import requests
import json
import random
from PIL import Image, ImageFont, ImageDraw
import textwrap
from nextcord import File, ButtonStyle, Embed, Color, SelectOption, Intents, Interaction, SlashOption
from nextcord.ui import Button, View, Select

links = json.load(open("gifs.json"))
helpGuide = json.load(open("help.json"))

# load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = 1028619109044326440

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')


def createHelpEmbed(pageNum=0, inline=False):
    pageNum = (pageNum) % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed = Embed(color=0x0080ff, title=pageTitle)
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name=bot.command_prefix+key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
    return embed


@bot.command(name="help")
async def Help(ctx):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    previousButton = Button(label="<", style=ButtonStyle.blurple)
    nextButton = Button(label=">", style=ButtonStyle.blurple)
    previousButton.callback = previous_callback
    nextButton.callback = next_callback

    myview = View(timeout=180)
    myview.add_item(previousButton)
    myview.add_item(nextButton)

    sent_msg = await ctx.send(embed=createHelpEmbed(currentPage), view=myview)


@bot.command(name="hi")
async def SendMessage(ctx):

    async def dropdown_callback(interaction):
        for value in dropdown.values:
            await ctx.send(random.choice(links[value]))

    option1 = SelectOption(label="chill", value="gif",
                           description="doggo is lonely", emoji="😎")
    option2 = SelectOption(label="play", value="play",
                           description="doggo is bored", emoji="🙂")
    option3 = SelectOption(label="feed", value="feed",
                           description="doggo is hungry", emoji="😋")
    dropdown = Select(placeholder="What would you like to do with doggo?", options=[
                      option1, option2, option3], max_values=3)
    dropdown.callback = dropdown_callback
    myview = View(timeout=180)
    myview.add_item(dropdown)

    await ctx.send('Hello! Are you bored?', view=myview)


@bot.command(name="pic")
async def pic(ctx):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_link = response.json()['message']
    await ctx.send(image_link)


@bot.command(name="gif", aliases=["feed", "play", "sleep"])
async def gif(ctx):
    await ctx.send(random.choice(links[ctx.invoked_with]))


# @bot.command(name='speak')
# async def speakOld(ctx, *args):
#     msg = " ".join(args)
#     font = ImageFont.truetype("PatrickHand-Regular.ttf", 50)
#     img = Image.open('dog.jpg')
#     cx, cy = (350, 230)

#     lines = textwrap.wrap(msg, width=20)
#     w, h = font.getsize(msg)
#     y_offset = (len(lines) * h)/2
#     y_text = cy - (h/2) - y_offset

#     for line in lines:
#         draw = ImageDraw.Draw(img)
#         w, h = font.getsize(line)
#         draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font)
#         img.save("dog-edited.jpg")
#         y_text += h
#     with open("dog-edited.jpg", "rb") as f:
#         img = File(f)
#         await ctx.channel.send(file=img)

@bot.slash_command(guild_ids=[GUILD_ID])
async def speak(interaction: Interaction, msg:str, fontSize: int = SlashOption(
        name="picker",
        choices={"30pt": 30, "50pt": 50, "70pt": 70},
    )):
	# msg = " ".join(args)

	font = ImageFont.truetype("PatrickHand-Regular.ttf", fontSize)
	img = Image.open("dog.jpg")
	cx, cy = (350, 230)
	
	lines = textwrap.wrap(msg, width=20)
	print(lines)
	w, h = font.getsize(msg)
	y_offset = (len(lines)*h)/2
	y_text = cy-(h/2) - y_offset

	for line in lines:
		draw = ImageDraw.Draw(img)
		w, h = font.getsize(line)
		draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font)
		img.save("dog-edited.jpg")
		y_text += h
	
	with open("dog-edited.jpg", "rb") as f:
		img = File(f)
		# await ctx.channel.send(file=img)
		# ephermal to hide msg
		await interaction.response.send_message(file=img, ephemeral=True)



@bot.command(name="support")
async def support(ctx):
    hi = Button(label="Click Me", style=ButtonStyle.blurple)
    tutorial = Button(label="Tutorial",
                      url="https://www.youtube.com/@Dannycademy")

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
        em = Embed(title="Slow it down bro!",
                   description=f"Try again in {error.retry_after:.2f}s", color=Color.red())
        await ctx.send(embed=em)


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
