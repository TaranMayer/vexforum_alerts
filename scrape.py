import discord
from discord.ext import commands
import bs4 as bs
from bs4 import BeautifulSoup, CData
import urllib.request
import time as Time
import asyncio
import mysql.connector
from urlextract import URLExtract
import hashlib
from threading import Thread
from queue import Queue
import difflib
import passwords
from async_class import AsyncClass

# Discord Setup
####################################################
client = commands.Bot(command_prefix = '!');       #
####################################################

# Variable Setup
###################################################
content = ""                                      #
author = ""                                       #
new_link = ""                                     #
old_link = ""                                     #
abbrvlink = ""                                    #
uploadpics = []                                   #
title = ""                                        #
time = ""                                         #
pfp = ""                                          #
urls = []                                         #
old_hash = ""                                     #
new_hash = ""                                     #
new_content_hash = ""                             #
old_content_hash = ""                             #
to_send = ""                                      #
deleted = '1d146def336a0b8d9479d3b70b94db0d'      #
channels = []                                     #
general = 734106468743249954                      #
channels.clear()                          #
feed_status = "old"                               #
old_content = ""                                  #
cody_channels = []                                #
cody = 734617775049539645                         #
cody_channels.append(cody)                        #
drow_channels = []                                #
drow = 734617775049539645                         #
drow_channels.append(drow)                        #
jpearman_channels = []                            #
jpearman = 734617775049539645                     #
jpearman_channels.append(jpearman)                #
num_hearts = ""                                   #
###################################################



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


class start_scrape(Thread):
    print("started class")
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        print("started self")
    def run(self):
        print("started scrape")
        # Variable Setup
        #################################
        global content                  #
        global author                   #
        global new_link                 #
        global old_link                 #
        global abbrvlink                #
        global uploadpics               #
        global title                    #
        global time                     #
        global pfp                      #
        global urls                     #
        global old_hash                 #
        global new_hash                 #
        global new_content_hash         #
        global to_send                  #
        global old_content_hash         #
        global client                   #
        global general                  #
        global feed_status              #
        global old_content              #
        global deleted                  #
        global num_hearts               #
        #################################
        while(True):
            try:
                try:
                    # Read VEX Forum and parse as html, generate hash for the feed
                    ###########################################################################
                    vf = urllib.request.urlopen('https://www.vexforum.com/posts.rss').read()  #
                    new_hash = hashlib.md5(str(vf).encode('utf-8')).hexdigest()               #
                    vf_html = BeautifulSoup(vf, 'html.parser')                                #
                    vf_xml = BeautifulSoup(vf, 'xml')                                         #
                    ###########################################################################
                except:
                    print("issue in reading or parsing URLS")
                    new_hash = old_hash

                if(new_hash != old_hash):
                    try:
                        # Finds content of the most recent post on the list
                        content = BeautifulSoup(vf_html.find('description').findNext('description').find(text=lambda t: isinstance(t, CData)), 'html.parser')
                        for img in content.select('img[alt]'):
                            img.replace_with(img['alt'])
                        content = content.text
                        new_content_hash = hashlib.md5(str(content).encode('utf-8')).hexdigest()
                        to_send = (content[:1000] + '') if len(content) > 75 else content
                        # Finds post GUID
                        guid = vf_html.find('guid').get_text(strip=True)
                        guid = guid[22:]
                        # Finds author of the most recent post on the list
                        author = vf_xml.find('creator').get_text(strip=True)
                        author = author.split()[0]
                        author = author[1:]
                        # Finds link and post ID
                        new_link = vf_xml.find('link').findNext('link').get_text(strip=True)
                        abbrvlink = new_link.split('/', 5)[5]
                        # Finds the links of all uploaded pictures
                        img_search = vf_xml.find('description').findNext('description').get_text(strip=True)
                        img_search = BeautifulSoup(img_search, 'html.parser')
                        for div in img_search.find_all("blockquote"):
                            div.decompose()
                        pics = img_search.findAll('img')
                        uploadpics = []
                        uploadpics.clear()
                        for pic in pics:
                            picstr = str(pic)
                            if not (picstr.find("avatar") != -1 or picstr.find("emoji") != -1):
                                embed_pic = pic.attrs['src']
                                embed_pic=str(embed_pic)
                                if(embed_pic.find("vexforum.com")!= -1):
                                    pass
                                else:
                                    embed_pic = "https://vexforum.com"+test_str
                                uploadpics.append(embed_pic)
                        # Finds title of topic
                        title = vf_html.find('title').findNext('title').text
                        # Finds timestamp
                        time = vf_html.find('item').text
                        num_lines = len(time.splitlines())
                        num_lines = num_lines - 2
                        time = time.splitlines()[num_lines]
                        time = time[:-5]
                        time = time[8:]
                        # Finds pfp image link and non-uploaded pictures
                        find_pfp = urllib.request.urlopen(f'https://www.vexforum.com/u/{author}').read()
                        find_img_link = urllib.request.urlopen(f'https://www.vexforum.com/raw/{abbrvlink}').read()
                        find_pfp = bs.BeautifulSoup(find_pfp, "html.parser")
                        find_pfp = find_pfp.find('img').findNext('img')
                        pfp = (find_pfp['src'])
                        find_img_link = str(find_img_link)
                        find_img_link = find_img_link[2:]
                        find_img_link = find_img_link[:-1]
                        quotenum = find_img_link.count('[/quote]')
                        try:
                            find_img_link = find_img_link.split("[/quote]")[quotenum].strip()
                        except:
                            print('no quotes')
                        try:
                            find_img_link = find_img_link.replace('\\n', '\n').replace('\\t', '\t')
                        except:
                            print('no newlines')
                        urls =URLExtract().find_urls(find_img_link)

                    except:
                        print("Issue in scraping data")
                    print(author)
                    try:
                        topic_num = abbrvlink[:5]
                        post_num = abbrvlink[6:]
                        post_num = int(post_num)
                        heart_url = urllib.request.urlopen(f'https://www.vexforum.com/t/{topic_num}/{post_num}').read()
                        heart_xml = BeautifulSoup(heart_url, 'lxml')
                        like_tags = heart_xml.findAll("span", {"class": "post-likes"})
                        hearts = []
                        hearts.clear()
                        for like_tag in like_tags:
                            likes = like_tag.get_text(strip=True)
                            if (likes == ""):
                                likes = "0 Likes"
                            hearts.append(likes)
                        if(post_num<=6):
                            num_hearts = hearts[post_num-1]
                            num_hearts = num_hearts[:-6]
                        else:
                            num_hearts = hearts[5]
                            num_hearts = num_hearts[:-6]
                        if(new_content_hash != old_content_hash and new_link != old_link and author != "system"):
                            sql = "SELECT content FROM posts WHERE content = %s"
                            mycursor.execute(sql, (to_send, ))
                            duplicates=mycursor.fetchone()
                            if(duplicates == None):
                                # New post was found
                                feed_status = "new"
                                sqlformula = "INSERT INTO posts (link, time, author, content, imglink, topic, edit, guid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                data = (abbrvlink, time, author, to_send, pfp, title, "0", guid)
                                mycursor.execute(sqlformula, data)
                                mydb.commit()
                            else:
                                print("A duplicate was found")
                            old_content_hash = new_content_hash
                            old_link=new_link

                        elif(new_content_hash != old_content_hash and new_link == old_link and author != "system"):
                            if(new_content_hash==deleted):
                                # Deleted post
                                feed_status = "delete"
                                sql = "SELECT edit FROM posts WHERE link = %s ORDER BY edit DESC LIMIT 1"
                                mycursor.execute(sql, (abbrvlink, ))
                                edits=mycursor.fetchone()
                                edits=str(edits)
                                edits = edits[2:]
                                edits = edits[:-3]
                                edits = int(edits)

                                sql = "SELECT content FROM posts WHERE link = %s ORDER BY edit DESC LIMIT 1"
                                mycursor.execute(sql, (abbrvlink, ))
                                old_content=mycursor.fetchone()
                                old_content=str(old_content)
                                old_content = old_content[2:]
                                old_content= old_content[:-3]
                                old_content = old_content.replace('\\n', '\n').replace('\\t', '\t')

                                sqlformula = "INSERT INTO posts (link, time, author, content, imglink, topic, edit, guid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                data = (abbrvlink, time, author, to_send, pfp, title, edits+1, guid)
                                mycursor.execute(sqlformula, data)
                                mydb.commit()
                                old_content_hash = new_content_hash
                                old_link=new_link
                            else:
                                print(new_content_hash)
                                print(deleted)
                                # Edited post

                                feed_status = "edit"
                                sql = "SELECT edit FROM posts WHERE link = %s ORDER BY edit DESC LIMIT 1"
                                mycursor.execute(sql, (abbrvlink, ))
                                edits=mycursor.fetchone()
                                edits=str(edits)
                                edits = edits[2:]
                                edits = edits[:-3]
                                edits = int(edits)

                                sql = "SELECT content FROM posts WHERE link = %s ORDER BY edit DESC LIMIT 1"
                                mycursor.execute(sql, (abbrvlink, ))
                                old_content=mycursor.fetchone()
                                old_content=str(old_content)
                                old_content = old_content[2:]
                                old_content= old_content[:-3]
                                old_content = old_content.replace('\\n', '\n').replace('\\t', '\t')

                                sqlformula = "INSERT INTO posts (link, time, author, content, imglink, topic, edit, guid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                data = (abbrvlink, time, author, to_send, pfp, title, edits+1, guid)
                                mycursor.execute(sqlformula, data)
                                mydb.commit()
                                old_content_hash = new_content_hash
                                old_link=new_link
                        else:
                            print("Hash stayed the same, but the link changed, or one of the other posts was edited, or system posted")
                        old_hash = new_hash
                    except:
                        print("Issue, likely in mySQL connection")
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

                Time.sleep(10)
            except:
                print("An unknown error occured in the scraping process")
start_scrape()
@client.event
async def on_ready():
    print("Ready!")
    # Variable Setup
    #################################
    global content                  #
    global author                   #
    global new_link                 #
    global old_link                 #
    global abbrvlink                #
    global uploadpics               #
    global title                    #
    global time                     #
    global pfp                      #
    global urls                     #
    global old_hash                 #
    global new_hash                 #
    global new_content_hash         #
    global to_send                  #
    global old_content_hash         #
    global client                   #
    global general                  #
    global feed_status              #
    global old_content              #
    global channels                 #
    #################################
    while(True):
        #try:
        if(feed_status == "new"):
            sql = "SELECT channel_id FROM channels"
            mycursor.execute(sql)
            channels_sending=mycursor.fetchall()
            for found_channel in channels_sending:
                found_channel = str(found_channel)
                found_channel = found_channel[:-3]
                found_channel = found_channel[2:]
                found_channel = int(found_channel)
                channels.append(found_channel)
            print("found new post from feed")
            try:

                embed=discord.Embed(color=0x3ed64b, url=new_link, title=f'{title}', description=f'{time}')
                embed.set_thumbnail(url=pfp)
                embed.add_field(name=f'New post from {author}:', value=f'{to_send}', inline=False)
                try:
                    if(len(urls)>0):
                        urls = ("\n".join(urls))
                        embed.add_field(name=f'Links in {author}\'s post:', value=f'{urls}', inline=False)
                except:
                    print("Error in adding links, maybe there were none?")
                for channel_to_send in channels:
                    send_channel = client.get_channel(channel_to_send)
                    await send_channel.send(embed=embed)
                    for picture in uploadpics:
                        await send_channel.send(picture)
            except:
                try:
                    print(f"Issue with posting. The post {abbrvlink} should still be in the database though")
                except:
                    print("Issue with posting. Ran into an issue with abbrvlink")
            feed_status = "old"
            channels.clear()
        elif(feed_status == "edit"):
            sql = "SELECT channel_id FROM channels"
            mycursor.execute(sql)
            channels_sending=mycursor.fetchall()
            for found_channel in channels_sending:
                found_channel = str(found_channel)
                found_channel = found_channel[:-3]
                found_channel = found_channel[2:]
                found_channel = int(found_channel)
                channels.append(found_channel)
            print("found edit from feed")
            try:
                diff = difflib.SequenceMatcher(isjunk=None, a=content, b=old_content)
                diff = diff.ratio()*100
                diff = float(diff)
                diff = 100-diff
                diff = round(diff, 3)

                embed=discord.Embed(color=0x33a5de, url=new_link, title=f'{title}', description=f'{time}')
                embed.set_thumbnail(url=pfp)
                embed.add_field(name=f'{author} edited their post. There is a {diff}% difference. New:', value=f'{to_send}', inline=True)
                embed.add_field(name=f":heart:x{num_hearts}", value="​", inline=True)
                embed.add_field(name='Old:', value=f'{old_content}', inline=False)
                for channel_to_send in channels:
                    send_channel = client.get_channel(channel_to_send)
                    await send_channel.send(embed=embed)
            except:
                try:
                    print(f"Issue with posting edit. The edit {abbrvlink} should still be in the database though")
                except:
                    print("Issue with posting edit. Ran into an issue with abbrvlink")
            feed_status = "old"
            channels.clear()
        elif(feed_status == "delete"):
            sql = "SELECT channel_id FROM channels"
            mycursor.execute(sql)
            channels_sending=mycursor.fetchall()
            for found_channel in channels_sending:
                found_channel = str(found_channel)
                found_channel = found_channel[:-3]
                found_channel = found_channel[2:]
                found_channel = int(found_channel)
                channels.append(found_channel)
            print("found delete from feed")
            try:
                embed=discord.Embed(color=0xde3341, url=new_link, title=f'{title}', description=f'{time}')
                embed.set_thumbnail(url=pfp)
                embed.add_field(name=f'{author} deleted their post. This is what it said:', value=f'{old_content}', inline=True)
                embed.add_field(name=f":heart:x{num_hearts}", value="​", inline=True)
                for channel_to_send in channels:
                    send_channel = client.get_channel(channel_to_send)
                    await send_channel.send(embed=embed)
            except:
                try:
                    print(f"Issue with posting delete. The delete {abbrvlink} should still be in the database though")
                except:
                    print("Issue with posting delete. Ran into an issue with abbrvlink")
            feed_status = "old"
            channels.clear()
        #except:
        #    print("Issue, likely with mySQL. Trying to reconnect")
        #    # Database Setup
        #    ########################################
        #    mydb = mysql.connector.connect(        #
        #        host = "freedb.tech",              #
        #        user = passwords.username,         #
        #        passwd = passwords.password,       #
        #        database = "freedb_vfsave"         #
        #    )                                      #
        #    mycursor = mydb.cursor(buffered=True)  #
        #    ########################################
        Time.sleep(5)


# Run bots
#####################################################################################################
                                                                                                    #
client.run(passwords.token)                                                                         #
                                                                                                    #
#####################################################################################################
