import discord
from discord.ext import commands
from pyTwistyScrambler import scrambler333
from scrambleupdate import *
from scrambles import *
acceptedmoves = ['U', 'D', 'R', 'L', 'F', 'B', 'Uw', 'Dw', 'Rw', 'Lw', 'Fw', 'Bw']


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Python: <a:gurawave:825157518363328512>")

    @commands.command()
    async def gcd(self, ctx):
      if len(ctx.message.content.split()) != 4:
        return await ctx.send("format: plz gcd <a> <b>")

      try:
        a = int(ctx.message.content.split()[2])
        b = int(ctx.message.content.split()[3])
      except ValueError:
        return await ctx.send("make sure both arguments are integers")

      steps = []

      def GCD(x, y):
          text = ""
          table = [(x, y)]
          while(y):
              steps.append((x, x//y, y, x % y))
              x, y = y, x % y
              table.append((x, y))
          table.pop()
          text += f'GCD is {x}\n\na\tb\ta = qb + r\n'
          for i in table:
              text += f"{i[0]}\t{i[1]}\t{i[0]} = {i[0] // i[1]} * {i[1]} + {i[0] % i[1]}\n"
          text += "\n"

          return text

      text = GCD(a, b)

      def LinearExp(steps):
          x = 0
          y = 1
          for i in reversed(steps):
              x1, y1 = x, y
              x = y1 - i[1] * x1
              y = x1

          return f"Linear Combination: {a} * {y} + {b} * {x} = {steps[-1][2]}"

      text += LinearExp(steps)

      await ctx.send(f"```{text}```")


    @commands.command(aliases=['caeser'])
    async def cshift(self, ctx):
        try:
          shift = int(ctx.message.content.split()[2])
        except ValueError:
          return await ctx.send("format plz cshift <shift> <text>")
        text = " ".join(ctx.message.content.split()[3:])
        if not isinstance(shift, int) or len(text) == 0:
          return await ctx.send("format plz cshift <shift> <text>")

        alpha = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]
        newtext = ""
        for i in text:
          if i in alpha:
            newtext += alpha[(alpha.index(i) + shift) % 26]
          else:
            newtext += i
        await ctx.send(f"`{newtext}`")
        
        

    @commands.command(aliases=['temp'])
    async def convert(self, ctx):
        temp = "".join(ctx.message.content.split()[2:]).replace(" ", "")

        if temp[-1].lower() == "f":
            await ctx.send(f"{round((float(temp[:-1])-32) * (5/9), 2)}° C")
        elif temp[-1].lower() == "c":
            await ctx.send(f"{round((float(temp[:-1]) * (9/5) + 32), 2)}° F")
            # ok bro actually not bad tho
            #you dont need to cast to string to send it with fstring woajj
            #rip this is doodobruho
            # dude i need to link to an api or something
            # and that's annoying it literally works fine ok
            # ok
            # i will figure out api later then will be easy to replicate that bot
            
    # @commands.command()
    # async def money(self, ctx, money, conversion):

    #     if conversion.lower() == "cad":
    #         await ctx.send(f"${round((float(money)/1.24), 2)} USD")
    #     if conversion.lower() == "usd":
    #         await ctx.send(f"${round((float(money)*1.24), 2)} CAD")

    @commands.command()
    async def avg(self, ctx):
        await ctx.send(round((sum([float(i) for i in ctx.message.content.split()[2:]]) - min([float(i) for i in ctx.message.content.split()[2:]]) - max([float(i) for i in ctx.message.content.split()[2:]])) / (len([float(i) for i in ctx.message.content.split(' ')[2:]]) - 2), 2))
    
    @commands.command(aliases=['1','1x1'])
    async def _1(self, ctx, amount: int = 1):
        if amount > 5: amount = 5
        for i in range(amount):
            await ctx.send(scramble1()) 

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def noob3(self, ctx):
        noobdict = {
            'U':'top', 'D':'bottom', 'R':'right', 'L':'left', 'F':'front', 'B':'back'
        }

        memestring = []
        msg = scrambler333.get_WCA_scramble()
        newmsg = msg.replace(' ','')
        m = len(newmsg) - 1
        while m > -1: 
            if newmsg[m] == "'":
                memestring.append('turn the ' + noobdict[newmsg[m-1]] + ' face counterclockwise by 90 degrees')
                m -= 2
            elif newmsg[m] == "2":
                memestring.append('turn the ' + noobdict[newmsg[m-1]] + ' face by 180 degrees')
                m -= 2
            elif newmsg[m] in acceptedmoves:
                memestring.append('turn the ' + noobdict[newmsg[m]] + ' face clockwise by 90 degrees')
                m -= 1
            else:
                return

        memestring = memestring[::-1]
        n = await ctx.send(', '.join(memestring))
        
        await n.add_reaction('🙃') 

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🙃'

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=10, check=check)
        except:
            await n.clear_reactions()
        else:
            file = scrambleimage(3, msg)
            file.save("scramble.png")
            await ctx.send(file = discord.File("scramble.png"))
            await n.clear_reactions()
    
    @commands.command(pass_context=True)
    async def setup(self, ctx):
        formattedstr = []
        msg = ctx.message.content[10:]
        msg = msg.replace("’", "'").replace("(", '').replace(")", '').replace(' ', '')

        if len(msg) > 0:
            m = len(msg) - 1
            while m > -1: 
                if msg[m] == "'":
                    if msg[m-1] == "2":
                        formattedstr.append(msg[m-2] + msg[m-1])
                        m -= 3
                    elif msg[m-1] in acceptedmoves:
                        formattedstr.append(msg[m-1])
                        m -= 2
                    else:
                        await ctx.send('invalid notation dud')
                        return
                elif msg[m] == "2":
                    formattedstr.append(msg[m-1] + msg[m])
                    m -= 2
                elif msg[m] in acceptedmoves:
                    formattedstr.append(msg[m] + "'")
                    m -= 1
                else:
                    await ctx.send('invalid notation dud')
                    return
        else: 
            await ctx.send('nothing to show bruh')
            return

        msg = formattedstr
        await ctx.send(' '.join(msg))

def setup(client):
    client.add_cog(Misc(client))

