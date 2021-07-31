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
    async def mal(self, ctx):
        links = []
        query = ("_".join(ctx.message.content.split()[2:])) # [2:]
        if not query:
            await ctx.send("Make sure to enter an anime")
            return

        page = requests.get("https://myanimelist.net/search/all?q=" + query + "&cat=all")
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
            await ctx.send(soup.find('a', class_='hoverinfo_trigger fw-b fl-l')['href'])
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

                url = "https://www.worldcubeassociation.org" + query
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                    
                stats_list = soup.get_text()[soup.get_text().find("Completed Solves") + 16:soup.get_text().find("Current Personal Records")].split("\n")

                try:
                  while True:
                    stats_list.remove('')
                except ValueError:
                  pass

                pfp = soup.find("img", {"class": "avatar"})['src']
                stats_list.append(pfp)

                name = soup.h2.string.strip()
                stats_list.append(name)

                embedVar = discord.Embed(title=stats_list[6] + "'s Profile", description="https://www.worldcubeassociation.org" + query, color=0x00ff00)
                embedVar.add_field(name="Country", value=stats_list[0], inline=True)
                embedVar.add_field(name="WCAID", value=stats_list[1], inline=True)
                embedVar.add_field(name="Gender", value=stats_list[2], inline=True)
                embedVar.add_field(name="Competitions", value=stats_list[3], inline=True)
                embedVar.add_field(name="Completed solves", value=stats_list[4], inline=True)
                embedVar.set_thumbnail(url=stats_list[5])
                await ctx.send(embed=embedVar)

            except:
                await ctx.send("No results found...")


def setup(client):
    client.add_cog(Queries(client))
