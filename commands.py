import discord
from discord.ext import commands
import bs4 as bs
from bs4 import BeautifulSoup, CData
import urllib.request
import time
import asyncio
import mysql.connector
from urlextract import URLExtract
from threading import Thread
import hashlib
import pprint
import passwords
client = commands.Bot(command_prefix = '.');

# Database Setup
########################################
mydb = mysql.connector.connect(        #
    host = "freedb.tech",              #
    user = passwords.username,         #
    passwd = passwords.password,       #
    database = "freedb_vfsave"         #
)                                      #
mycursor = mydb.cursor(buffered=True)  #
########################################


@client.event
async def on_ready():
    print("Ready!")

@client.command()
async def check(ctx):
    author_id = ctx.message.author.id
    if(author_id == 332184957910777857):
        sql = "SELECT channel_id FROM channels"
        mycursor.execute(sql)
        channels=mycursor.fetchall()
        await ctx.send("Sent a test message to all channels on the channel list!")
        for channel in channels:
            channel = str(channel)
            channel = channel[:-3]
            channel = channel[2:]
            channel = int(channel)
            print(channel)
            sending = client.get_channel(channel)
            await sending.send(f"This is a check to make sure the bot is sending messages correctly")
    else:
        await ctx.send("You don't have the authorization to do that!")


@client.command()
async def add(ctx):
    author_name = ctx.message.author.name
    author_id = ctx.message.author.id
    channel_id = ctx.channel.id
    channel_name = ctx.message.channel.name
    server_name = ctx.message.guild.name
    server_id = ctx.message.guild.id

    sql = f'''SELECT channel_id FROM channels WHERE channel_id = "{channel_id}"'''
    mycursor.execute(sql)
    channels=mycursor.fetchone()

    if(channels == None):
        sqlformula = "INSERT INTO channels (author_name, author_id, server_name, server_id, channel_name, channel_id) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (author_name, author_id, server_name, server_id, channel_name, channel_id)
        mycursor.execute(sqlformula, data)
        mydb.commit()
        await ctx.send(f'`{author_name}` added `{channel_name}` in `{server_name}` to general post subscription list')
    else:
        await ctx.send(f'This channel is already on the general post subscription list')


@client.command()
async def remove(ctx):
    author_name = ctx.message.author.name
    author_id = ctx.message.author.id
    channel_id = ctx.channel.id
    channel_name = ctx.message.channel.name
    server_name = ctx.message.guild.name
    server_id = ctx.message.guild.id

    sql = f'''SELECT channel_id FROM channels WHERE channel_id = "{channel_id}"'''
    mycursor.execute(sql)
    channels=mycursor.fetchone()

    if(channels != None):
        sqlformula = f'''DELETE FROM channels WHERE channel_id = "{channel_id}"'''
        mycursor.execute(sqlformula)
        mydb.commit()
        await ctx.send(f'`{author_name}` removed `{channel_name}` in `{server_name}` from general post subscription list')
    else:
        await ctx.send(f'This channel is not on the general post subscription list')

@client.command()
async def SELECT(ctx, arg1, arg2, arg3):
    print(arg1)
    print(arg2)
    print(arg3)
    check_str = str(arg1)+str(arg2)+str(arg3)
    if(check_str.find("-") != -1 or check_str.find(";") != -1 or check_str.find("*") != -1):
        await ctx.send("Sorry, requests can't contain the characters `-`, `;`, or `*` for security reasons.")
    else:
        try:
            query = f'''SELECT {arg1} FROM posts WHERE {arg2} = "{arg3}"'''
            mycursor.execute(query)
            results=mycursor.fetchall()
        except:
            await ctx.send("Sorry, there was an issue in your command. You can send them in this format: \n .SELECT <data field> <parameter> <value> ")
        try:
            for result in results:
                result = str(result)
                result = result[:-3]
                result = result[2:]
                await ctx.send(result)
        except:
            pass

@client.command()
async def refresh(ctx):
    # Database Setup
    ########################################
    mydb = mysql.connector.connect(        #
        host = "freedb.tech",              #
        user = passwords.username,         #
        passwd = passwords.password,       #
        database = "freedb_vfsave"         #
    )                                      #
    mycursor = mydb.cursor(buffered=True)  #
    ########################################
    query = "SELECT version()"
    mycursor.execute(query)
    results=mycursor.fetchone()
    results = str(results)
    results = results[:-3]
    results = results[2:]
    await ctx.send(f"Connection to SQL Server refreshed! Running on {results}")

@client.command()
async def report(ctx):
    # Database Setup
    ########################################
    mydb = mysql.connector.connect(        #
        host = "freedb.tech",              #
        user = passwords.username,         #
        passwd = passwords.password,       #
        database = "freedb_vfsave"         #
    )                                      #
    mycursor = mydb.cursor(buffered=True)  #
    ########################################
    query = f'''SELECT link FROM posts ORDER BY time DESC'''
    mycursor.execute(query)
    results=mycursor.fetchmany(100)
    print(len(results))
    all_links = []
    all_links.clear()
    for result in results:
        result = str(result)
        result = result[:-3]
        result = result[2:]
        if result in all_links:
            pass
        else:
            all_links.append(result)


    for link in all_links:
        try:
            try:
                print(link)
                vf = urllib.request.urlopen(f'https://www.vexforum.com/raw/{link}').read()
                vf_html = BeautifulSoup(vf, 'html.parser')
                post_str = str(vf_html)
                if(post_str.find("(post withdrawn by author, will be automatically deleted in 24 hours unless flagged)") != -1):
                    print(f"found delete {link}")
                    deletesql = f'''SELECT content FROM posts WHERE link = "{link}" ORDER BY edit DESC LIMIT 0,1'''
                    mycursor.execute(deletesql)
                    deletedcontent = mycursor.fetchone()
                    deletedcontent = str(deletedcontent)
                    deletedcontent = deletedcontent[2:]
                    deletedcontent = deletedcontent[:-3]
                    deletedcontent = deletedcontent.replace('\\n', '\n').replace('\\t', '\t')
                    deletedcontent = (deletedcontent[:1000] + '') if len(deletedcontent) > 75 else deletedcontent
                    deletesql = f'''SELECT author FROM posts WHERE link = "{link}" ORDER BY edit DESC LIMIT 0,1'''
                    mycursor.execute(deletesql)
                    deletedauthor = mycursor.fetchone()
                    deletedauthor = str(deletedauthor)
                    deletedauthor = deletedauthor[2:]
                    deletedauthor = deletedauthor[:-3]
                    deletedauthor = deletedauthor.replace('\\n', '\n').replace('\\t', '\t')
                    deletesql = f'''SELECT time FROM posts WHERE link = "{link}" ORDER BY edit DESC LIMIT 0,1'''
                    mycursor.execute(deletesql)
                    deletedtime = mycursor.fetchone()
                    deletedtime = str(deletedtime)
                    deletedtime = deletedtime[2:]
                    deletedtime = deletedtime[:-3]
                    deletedtime = deletedtime.replace('\\n', '\n').replace('\\t', '\t')
                    deletesql = f'''SELECT imglink FROM posts WHERE link = "{link}" ORDER BY edit DESC LIMIT 0,1'''
                    mycursor.execute(deletesql)
                    deletedlink = mycursor.fetchone()
                    deletedlink = str(deletedlink)
                    deletedlink = deletedlink[2:]
                    deletedlink = deletedlink[:-3]
                    deletedlink = deletedlink.replace('\\n', '\n').replace('\\t', '\t')
                    deletesql = f'''SELECT topic FROM posts WHERE link = "{link}" ORDER BY edit DESC LIMIT 0,1'''
                    mycursor.execute(deletesql)
                    deletedtopic = mycursor.fetchone()
                    deletedtopic = str(deletedtopic)
                    deletedtopic = deletedtopic[2:]
                    deletedtopic = deletedtopic[:-3]
                    deletedtopic = deletedtopic.replace('\\n', '\n').replace('\\t', '\t')


                    embed=discord.Embed(color=0xeb4034, title=f'{deletedtopic}', description=f'{deletedtime}')
                    embed.set_thumbnail(url=deletedlink)
                    embed.add_field(name=f"{deletedauthor} deleted their post. This is what it said:", value=f'{deletedcontent}', inline=False)

                    sql = "SELECT channel_id FROM channels"
                    mycursor.execute(sql)
                    channels=mycursor.fetchall()
                    for channel in channels:
                        channel = str(channel)
                        channel = channel[:-3]
                        channel = channel[2:]
                        channel = int(channel)
                        sending = client.get_channel(channel)
                        await sending.send(embed=embed)

            except:
                print(f"couldn't find {link}")
                deletesql = f'''SELECT content FROM posts WHERE link = "{link}" ORDER BY edit DESC'''
                mycursor.execute(deletesql)
                deletedcontent = mycursor.fetchone()
                deletedcontent = str(deletedcontent)
                deletedcontent = deletedcontent[2:]
                deletedcontent = deletedcontent[:-3]
                deletedcontent = deletedcontent.replace('\\n', '\n').replace('\\t', '\t')
                deletedcontent = (deletedcontent[:1000] + '') if len(deletedcontent) > 75 else deletedcontent
                deletesql = f'''SELECT author FROM posts WHERE link = "{link}" ORDER BY edit DESC'''
                mycursor.execute(deletesql)
                deletedauthor = mycursor.fetchone()
                deletedauthor = str(deletedauthor)
                deletedauthor = deletedauthor[2:]
                deletedauthor = deletedauthor[:-3]
                deletedauthor = deletedauthor.replace('\\n', '\n').replace('\\t', '\t')
                deletesql = f'''SELECT time FROM posts WHERE link = "{link}" ORDER BY edit DESC'''
                mycursor.execute(deletesql)
                deletedtime = mycursor.fetchone()
                deletedtime = str(deletedtime)
                deletedtime = deletedtime[2:]
                deletedtime = deletedtime[:-3]
                deletedtime = deletedtime.replace('\\n', '\n').replace('\\t', '\t')
                deletesql = f'''SELECT imglink FROM posts WHERE link = "{link}" ORDER BY edit DESC'''
                mycursor.execute(deletesql)
                deletedlink = mycursor.fetchone()
                deletedlink = str(deletedlink)
                deletedlink = deletedlink[2:]
                deletedlink = deletedlink[:-3]
                deletedlink = deletedlink.replace('\\n', '\n').replace('\\t', '\t')
                deletesql = f'''SELECT topic FROM posts WHERE link = "{link}" ORDER BY edit DESC'''
                mycursor.execute(deletesql)
                deletedtopic = mycursor.fetchone()
                deletedtopic = str(deletedtopic)
                deletedtopic = deletedtopic[2:]
                deletedtopic = deletedtopic[:-3]
                deletedtopic = deletedtopic.replace('\\n', '\n').replace('\\t', '\t')


                embed=discord.Embed(color=0x7851a9, title=f'{deletedtopic}', description=f'{deletedtime}')
                embed.set_thumbnail(url=deletedlink)
                embed.add_field(name=f"{deletedauthor}'s post was removed. This is what it said:", value=f'{deletedcontent}', inline=False)

                sql = "SELECT channel_id FROM channels"
                mycursor.execute(sql)
                channels=mycursor.fetchall()
                for channel in channels:
                    channel = str(channel)
                    channel = channel[:-3]
                    channel = channel[2:]
                    channel = int(channel)
                    sending = client.get_channel(channel)
                    await sending.send(embed=embed)
        except:
            print("unknown error in reporting")

client.run(passwords.token)
