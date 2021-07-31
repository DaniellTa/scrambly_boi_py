# for on_message event 3bld/4bld/5bld

scrambleCommands = {
    'plz 3bld': scrambler333.get_3BLD_scramble,
    'plz 4bld': scrambler444.get_4BLD_scramble,
    'plz 5bld': scrambler555.get_5BLD_scramble,
}

# ---
channel = message.channel
messageSplit = message.content.lower().split()

if message.author.id == bot.user.id:
	return

try:
	scrambleCommands[(messageSplit[0] + ' ' + messageSplit[1])]
except:
	return

if len(messageSplit) > 2:
	amt = int(messageSplit[-1])
	if amt > 5: amt = 5
else:
	amt = 1

for i in range(amt):
	embed = discord.Embed(title = '', description = scrambleCommands[(messageSplit[0] + ' ' + messageSplit[1])](), color = 0x43a8ff)
	await channel.send(embed = embed)


# old show command only used for 3x3
@commands.command(pass_context=True)
async def show(self, ctx):
	formattedstr = []
	removedslash = []
	msg = ctx.message.content[9:]

	for line in msg.splitlines():
		slashes = [i for i in range(len(line)) if line.startswith('//', i)]
		if len(slashes) > 0:
			r = line.replace(line[slashes[0]:],'')
			removedslash.append(r)
		else:
			removedslash.append(line)

	msg = ' '.join(removedslash)
	msg = msg.replace("’", "'").replace("(", '').replace(")", '').replace(' ', '')
	msg = msg.replace('Rw','r').replace("Lw",'l').replace("Uw",'u').replace("Dw",'d').replace("Fw",'f').replace("Bw",'b')
	if len(msg) > 0:
		m = len(msg) - 1
		while m > -1: 
			if msg[m] == "'":
				if msg[m-1] == "2":
					formattedstr.append(msg[m-2] + msg[m-1] + msg[m])
					m -= 3
				elif msg[m-1] in acceptedmoves:
					formattedstr.append(msg[m-1] + msg[m])
					m -= 2
				else:
					await ctx.send('invalid notation dud1')
					return
			elif msg[m] == "2":
				if msg[m-1] in acceptedmoves:
					formattedstr.append(msg[m-1] + msg[m])
					m -= 2
				elif msg[m-1] == 'w':
					await ctx.send('use lowercase notation for wide moves plz')
					return
				else:
					await ctx.send('invalid notation dud2')
					return
			elif msg[m] in acceptedmoves:
				formattedstr.append(msg[m])
				m -= 1
			else:
				await ctx.send('invalid notation dud')
				return
	else: 
		await ctx.send("nothing to show bruh (e.g, \"plz show R U R' U'\")")
		return

	msg = formattedstr[::-1]
	msg.append(' ')
	base = await ctx.send(' '.join(msg) + '\n' + input3([]))
	await base.add_reaction('👀')
	
	def check(reaction, user):
		return user == ctx.author and str(reaction.emoji) == '👀'

	movecounter = 1
	for move in msg:
		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout = 1, check=check)
		except:
			await base.edit(content= str(' '.join(msg[:movecounter-1])) + ' ' + "**{}**".format(''.join(str(msg[movecounter-1]))) + ' ' + str(' '.join(msg[movecounter:])) + ' ' + '\n' + input3(msg[:movecounter]))
			movecounter += 1
		else:
			await base.edit(content = ' '.join(msg) + '\n' + input3(msg))
			await base.clear_reactions()
			return

	await base.clear_reactions()	

  #-----------------------------------------------
  # cogs.queries.py
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import requests


class Queries(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tcs(self, ctx):
        links = []
        query = "+".join(ctx.message.content.split()[2:])
        if not query:
            await ctx.send("Make sure to enter a search query.")
            return

        page = requests.get("https://www.thecubicle.com/search?type=product&q=" + query)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
            await ctx.send("https://www.thecubicle.com/" + soup.find('a', class_='product-grid-item')['href'])
        except TypeError:
            await ctx.send("No results found...")

    @commands.command()
    async def scss(self, ctx):
        links = []
        query = "+".join(ctx.message.content.split()[2:])
        if not query:
            await ctx.send("Make sure to enter a search query.")
            return

        page = requests.get("https://www.speedcubeshop.com/search?type=product&q=" + query)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
            await ctx.send("https://www.speedcubeshop.com/" + soup.find('a', class_='product-title')['href'])
        except TypeError:
            await ctx.send("No results found...")

    @commands.command()
    async def wcaid(self, ctx):
        name = "+".join(ctx.message.content.split()[2:])
        if not name:
            await ctx.send("Be sure to enter a name to search up")
        else:
            url = ("https://www.worldcubeassociation.org/search?q=" + str(name)).replace(" ","%20")
            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            try:
                query = soup.find("table",{"class":"table table-nonfluid table-vertical-align-middle"}).a["href"]
                await ctx.send("https://www.worldcubeassociation.org" + query)
            except:
                await ctx.send("No results found...")


def setup(client):
    client.add_cog(Queries(client))

