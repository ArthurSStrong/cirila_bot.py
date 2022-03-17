import time
import discord
import psutil
import os
import random

from discord.ext import commands
from utils import permissions, default, http

#from lib.imgur import Imgur


class Huachiapi:

    description = "description"
    default_msg = "Holis aún estoy bajo construcción!"

    def __init__(self):
        pass

    # saldazo method
    def saldazo(self, *args):
        return f"{self.default_msg}"

    # shop method
    def shop(self, *args):
        if args[0] == 'frase_piolinera':
            return
        elif args[0] == 'piolin':
            #return Imgur().get_image("piolin")
            return f"{self.default_msg}" 
        else:
            return f"{self.default_msg}"

    # TTip method
    def tip(self, *args):
        return f"<:huachi:809238593696432200>"


class Huachinet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())
        self.api = Huachiapi()

    @commands.command()
    @commands.check(permissions.is_owner)
    async def estasviva(self, ctx):
        """ Simón! """
        before = time.monotonic()
        message = await ctx.send("Por su pollo!")

    @commands.command(aliases=["borrar-mensajes", "borrar"])
    @commands.check(permissions.is_owner)
    async def limpiar(self, ctx, amount):
        """ Check out my source code <3 """
        if amount is None:
            await ctx.channel.purge(limit=5)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))
        await ctx.send("Listo Jefe ;)")


    @commands.command(aliases=["saldo", 'saldazo'])
    @commands.check(permissions.is_owner)
    async def damesaldo(self, ctx):
        """ Consulta tu saldo """
        response = self.api.saldazo(None)
        await ctx.send(response)


    @commands.command(aliases=["comprar"])
    @commands.check(permissions.is_owner)
    async def shop(self, ctx, *args):
        """ Compra algo de la huachinet """
        try:
            response = self.api.shop(args[0])
        except:
            response = self.api.shop(None)
        await ctx.send(response)


    @commands.command(aliases=["propina"])
    @commands.check(permissions.is_owner)
    async def tip(self, ctx):
        """ Dale propina a alguien """
        response = self.api.tip(None)
        await ctx.send(response)


    @commands.command(aliases=["chocorrol", 'dar-role'])
    @commands.guild_only()
    async def role(self, ctx, user: discord.Member, *, role: discord.Role):
        """ Ya no hay chocorroles """
        if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
            await ctx.send('**:x: | Este rol es superior al tuyo!**')
        if role in user.roles:
            await user.remove_roles(role)  # removes the role if user already has
            await ctx.send(f"Removido {role} de {user.mention}")
        else:
            await user.add_roles(role)  # adds role if not already has it
            await ctx.send(f"Añadido {role} a {user.mention}")


    @commands.command(aliases=["levanton", 'asalto'])
    @commands.check(permissions.is_owner)
    async def atraco(self, ctx):
        """ Atraco hijodetuputamadre """
        if (guild := ctx.message.guild) is None or ctx.message.author.bot:
            return
        me = guild.me

        if ctx.message.reference is None:
            await ctx.send("Ni robar sabes wey!!")
            return

        print(ctx.message.reference.message_id)

        reference_msg = await ctx.fetch_message(ctx.message.reference.message_id)

        try:
            victim = reference_msg.author.id
            print(victim)
            if reference_msg.author == me:
                response = "A mi no me robas wey!!"
            elif victim == ctx.author.id:
                response = "No te puedes robar a ti mismo wey!!"
            else:
                currency_string = "${:,.2f}".format(
                    float(random.randrange(0, 1999)))
                response = "{} robó {} <:huachi:809238593696432200> de la cartera de {}".format(
                    ctx.author.mention, currency_string, reference_msg.author.mention)
            await ctx.send(response)
        except Exception as e:
            print(e)

    @commands.command(aliases=["huachilate", "raspadito"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def huachito(self, ctx):
        """ Prueba tu suerte """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

async def setup(bot):
    await bot.add_cog(Huachinet(bot))
