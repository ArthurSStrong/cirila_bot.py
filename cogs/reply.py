from utils import default
from discord.ext import commands
from discord import Message, TextChannel, Thread
from utils import textreplies
import discord
import os
import random
import psutil

class Reply(commands.Cog):
    '''
    Reply oject is a cog for the discord.py bot class it extends from it
    :param bot: discord.py bot object
    '''
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())
        self.affection_triggers = textreplies.get_af_det()
        self.affection_responses = textreplies.get_af_resp()
        self.chat_replies = textreplies.get_chat_replies()
        self.replies = textreplies.get_replies()
        self.default_responses = textreplies.get_def_resp()

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        '''on_message async function will listen to chat comments in discord trhu cog.listener decorator
        it uses the textreplies statics functions to read the list of responses from txt and csv files

        Args:
            message (Message): discord.py Message Object
        '''
        #print("on_message")
        if (guild := message.guild) is None or message.author.bot:
            return
        channel = message.channel
        me = guild.me
        assert isinstance(channel, (TextChannel, Thread))
        assert isinstance(me, discord.Member)
        if not channel.permissions_for(me).send_messages:
            return

        r = random.randint(1, 10000)
        _chance = r / 1.17

        if _chance > 9998:
            await channel.send("https://cdn.discordapp.com/attachments/821542780730998844/869682132316995635/image0-1-1-1-1-1.png")
            await self.bot.process_commands(message)

        if me.mentioned_in(message):
            if any(map(message.content.lower().__contains__, self.affection_triggers)):
                resp = random.choice(self.affection_responses)
                await channel.send(resp)
            elif resp := textreplies.get_any_dict(self.replies, message.content.lower()):
                await channel.send(resp)
            else:
                resp = random.choice(self.default_responses)
                await channel.send(resp)
        else:
            if resp := textreplies.get_any_dict(self.chat_replies, message.content.lower()):
                await channel.send(resp)


def setup(bot):
    bot.add_cog(Reply(bot))
