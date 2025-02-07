import random
import discord
import secrets
import asyncio
import aiohttp

from io import BytesIO
from discord.ext import commands
from utils import permissions, http, default


class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()

    @commands.command(aliases=["dime-cirila"])
    @commands.has_role("Mujicano")
    async def dimecirila(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        ballresponse = [
            "Simón", "Nel", "Al chile quien sabe...", "Lo dudo bebé..",
            "A huevo!", "Sin duda", "Parece que si", "Tal vez",
            "Ya callate wey", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;"
        ]

        answer = random.choice(ballresponse)
        await ctx.send(f"🎱 **Le preguntaste a Cirila:** {question}\n**Cirila dice:** {answer}")

    async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
        try:
            r = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])

    async def api_img_creator(self, ctx, url: str, filename: str, content: str = None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if not req:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def patas(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coffee(self, ctx):
        """ Posts a random coffee """
        await self.randomimageapi(ctx, "https://coffee.alexflipnote.dev/random.json", "file")

    @commands.command(aliases=["flip", "coin"])
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Cara", "Cruz"]
        await ctx.send(f"**{ctx.author.name}** lanzó una moneda y cayó:  **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** ha presionado [F] para mostrar su respeto! {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to your words """
        async with ctx.channel.typing():
            try:
                url = await http.get(f"https://api.urbandictionary.com/v0/define?term={search}", res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url["list"]):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    # @commands.command()
    # async def password(self, ctx, nbytes: int = 18):
    #     """ Generates a random password string for you

    #     This returns a random URL-safe text string, containing nbytes random bytes.
    #     The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
    #     """
    #     if nbytes not in range(3, 1401):
    #         return await ctx.send("I only accept any numbers between 3-1400")
    #     if hasattr(ctx, "guild") and ctx.guild is not None:
    #         await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
    #     await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command()
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def comprarcerveza(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: A huevoooooooo!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*Se bebe una cheve contigo* 🍻")
        if user.bot:
            return await ctx.send(f"Me gustaria darle un cheve a  **{ctx.author.name}**, pero los bots no toman cheve :/")

        beer_offer = f"**{user.name}**, le ofrecieron una cheve  🍺 de parte de **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["es-sexy", "es-hot"])
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def sexyono(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** es **{hot:.2f}%** sepsi {emoji}")

    @commands.command(aliases=["notame-sempai"])
    @commands.has_role("Mujicano")
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("I cannot send images here ;-;")

        bio = BytesIO(await http.get("https://i.alexflipnote.dev/500ce4.gif", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))


    @commands.command(aliases=["slots", "bet"])
    @commands.has_role("Mujicano")
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a, b, c = [random.choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


async def setup(bot):
    await bot.add_cog(Fun_Commands(bot))
